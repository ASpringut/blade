from django.conf.urls import patterns, include, url
from recipes.views import *


urlpatterns = patterns('',

    url(r'^add/$', add_recipe),
    url(r'^view/$', view_recipes),
    url(r'^view_recipe/$', view_recipe, name="view_recipe"),
    url(r'^serve/$', serve_recipe),
    url(r'^view_service/$', view_service),
    
)