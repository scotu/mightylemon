from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date

class Event(models.Model):
    """
    Represents an event you're attending.
    """
    name = models.CharField(_("name"), max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(_("description"))
    location = models.CharField(_("location"), max_length=150)
    start_date = models.DateField(_("start date"), default=date.today)
    end_date = models.DateField(_("end date"), blank=True, null=True)
    link_to_url = models.URLField(_("link to url"), max_length=250, blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]
       
    def is_old(self):
        if self.start_date < date.today():
            return True
        return False
    
    def __unicode__(self):
        return _("%(event_name)s on %(event_date)s") % {"event_name": self.name, "event_date": self.start_date}

