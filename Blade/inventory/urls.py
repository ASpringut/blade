from django.conf.urls import patterns, include, url
from inventory.views import *


urlpatterns = patterns('',


    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^main/$', resturantMain),
    url(r'^register/$', register),
    url(r'^ingredient/$', ingredient),
    url(r'^recipes/$', recipes),
    
)