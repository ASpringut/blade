from django.conf.urls import patterns, include, url
from inventory.views import *


urlpatterns = patterns('',

    url(r'^view/$', ingredient),
    url(r'^add/$', add_ingredients),
    url(r'^redirect/$', ingredient_redirect),
    url(r'^print/$', print_view),
)