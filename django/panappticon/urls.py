from django.conf.urls.defaults import *

urlpatterns = patterns("panappticon.views",
    url(r"^$", "index", name="panappticon_index"),
    url(r"^iphone_upload/$", "iphone_upload"),
    url(r"^user/(?P<id>\d+)/$", "user", name="user"),
)
