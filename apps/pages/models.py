from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from blog.models import Blog


class PageManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Page(models.Model):
    blog = models.ForeignKey(Blog, related_name=_("pages"))
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    body = models.TextField(_("body"))
    markup_type = models.CharField(max_length=10, choices=(
        ("html", "HTML"),
        ("rst", "reStructuredText"),
        ("markdown", "Markdown"),
    ), default="html")
    active = models.BooleanField(default=False)
    create_date = models.DateTimeField(_("created"), default=datetime.now)
    pub_date = models.DateTimeField(_("published"), default=datetime.now)
    permalink = models.CharField(_("permalink"), max_length=50, blank=True, null=True)
    enable_comments = models.BooleanField(default=True)
    tags = TagField()
    
    objects = PageManager()

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        ordering = ("-pub_date",)

    def get_absolute_url(self):
        if self.permalink:
            return self.permalink
        return "/%s/" % self.slug