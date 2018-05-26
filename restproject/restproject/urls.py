
from django.conf.urls import url
from django.contrib import admin
from users.views import *
from event.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/$', UsersData.as_view()),
    url(r'^login/$', UserLogin.as_view()),
    url(r'^verifytoken/$', TokenAuthentication.as_view()),
    url(r'^events/$', Events.as_view()),
    url(r'^events/(\d+)/$', Events.as_view()),
    url(r'^events/(\d+)/description/$', Events.as_view()),
]