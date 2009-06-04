
from datetime import datetime
from django.db import models
from django.conf import settings
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag
from tagging.fields import TagField
from mailer import send_mail
from comment_utils.moderation import CommentModerator, moderator
import settings

class Blog(models.Model):
    title = models.CharField(_("title"), max_length=100)
    author = models.ForeignKey(User, related_name="author", verbose_name=_("author"))
    theme = models.CharField(max_length=100, choices=settings.THEME_CHOICES, default=settings.DEFAULT_THEME,
        help_text=_("Select from the default themes."))
    theme_path = models.CharField(max_length=400, null=True, blank=True, help_text=_("Optional full path to \
        custom theme directory. If left blank, the blog theme option will be used."))

    def __unicode__(self):
        return self.title

    def get_archive_years(self):
        dates = Post.objects.dates('pub_date', 'year', order="DESC")
        return [date.year for date in dates]

    @property
    def settings(self):
        try:
            return self.blogsettings_set.all()[0]
        except IndexError:
            settings = BlogSettings(blog=self)
            settings.save()
            return settings


class BlogSettings(models.Model):
    # Good enough for now
    blog = models.ForeignKey(Blog)
    posts_per_page = models.PositiveIntegerField(_("posts per page"), default=6)

    class Meta:
        verbose_name_plural = _("blog settings")

    def __unicode__(self):
        return _("%(blog_title)s settings") % {"blog_title": self.blog.title}


class PostManager(models.Manager):
    def active(self):
        return self.filter(active=True)
        

class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name="posts", verbose_name=_("blog"))
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    body = models.TextField(_("body"))
    markup_type = models.CharField(max_length=10, choices=(
        ("html", "HTML"),
        ("rst", "reStructuredText"),
        ("markdown", "Markdown"),
    ), default="html")
    active = models.BooleanField(_("active"), default=False)
    create_date = models.DateTimeField(_("created"), default=datetime.now)
    pub_date = models.DateTimeField(_("published"), default=datetime.now)
    permalink = models.CharField(_("permalink"), max_length=50, blank=True, null=True)
    enable_comments = models.BooleanField(_("enable comments"), default=True)
    tags = TagField()
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-pub_date",)
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {
            "year": self.pub_date.strftime("%Y"),
            "month": self.pub_date.strftime("%b").lower(),
            "day": self.pub_date.strftime("%d"),
            "slug": self.slug,
        })
        

class PostModerator(CommentModerator):
    akismet = True
    email_notification = True
    enable_field = "enable_comments"
    
    def email(self, comment, content_object):
        """
        Use django-mailer for mail delivery.
        """
        if self.email_notification and not comment.is_public:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template("comment_utils/comment_notification_email.txt")
        ctx = Context({
            "comment": comment,
            "content_object": content_object,
            "site": Site.objects.get_current(),
        })
        subject = _('[%(site_name)s] Comment: "%(content_object)s"') % {
            "site_name": Site.objects.get_current().name,
            "content_object": content_object
        }
        message = t.render(ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

moderator.register(Post, PostModerator)
