from django.conf.urls import patterns, include, url
from users.views import *

urlpatterns = patterns('',

    url(r'^$', index),
    url(r'^main/$', resturantMain),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^register/$', register),

)