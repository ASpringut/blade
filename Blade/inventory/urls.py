from django.conf.urls import patterns, include, url
from inventory.views import *


urlpatterns = patterns('',

    url(r'^view/$', ingredient),
    url(r'^add/$', add_ingredients),
)