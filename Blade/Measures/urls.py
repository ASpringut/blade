from django.conf.urls import patterns, include, url
from Measures.views import *


urlpatterns = patterns('',

    url(r'^ajax/getunit$', get_units),
    
)

