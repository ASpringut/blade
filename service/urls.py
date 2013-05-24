from django.conf.urls import patterns, include, url
from service.views import *

urlpatterns = patterns('',

    url(r'^serve/$', serve_recipe),
    url(r'^view_service/$', view_service),

)