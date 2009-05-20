from django.conf.urls.defaults import *
from pages.models import Page
from django.conf import settings

try:
    template_name = settings.PAGE_TEMPLATE_NAME
except AttributeError:
    template_name = "page.html"

urlpatterns = patterns("")

# Create urls for every active Page
for page in Page.objects.active():
    urlpatterns += patterns("django.views.generic.simple",
        url(r"^%s$" % page.get_absolute_url().lstrip('/'),
            "direct_to_template", {"template": template_name, "extra_context": {"page": page}}
        ),
    )