from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    Not everyone is Brian Rosner.
    """
    user = models.ForeignKey(User, unique=True, verbose_name=_("user"))

    full_name = models.CharField(_("full name"), max_length=60, blank=True)
    nickname = models.CharField(_("nickname"), max_length=30, blank=True)
    about_me = models.TextField(_("about me"), blank=True)
    
    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
    
    def __unicode__(self):
        if self.full_name and self.nickname:
            return "%s (%s)" % (self.full_name, self.nickname,)
        elif self.nickname:
            return self.nickname
        elif self.fullname:
            return self.full_name
        else:
            return _("user profile #%(id)s") % {"id": self.pk}
