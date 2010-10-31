from django.conf.urls.defaults import *

urlpatterns = patterns(
    "panappticon.views",
    url(r"^$", "index", name="panappticon_index"),
    url(r"^iphone_upload/$", "iphone_upload"),
    url(r"^user/(?P<id>\d+)/$", "user", name="user"),
    url(r"^user_edit/(?P<id>\d+)/$", "user_edit", name="user_edit"),
    url(r"^session/(?P<id>\d+)/$", "session", name="session"),
)
