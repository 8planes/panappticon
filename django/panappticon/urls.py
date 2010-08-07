from django.conf.urls.defaults import *

urlpatterns = patterns("panappticon.views",
    url(r"^$", "index", name="panappticon_index"),
)
