from django.conf.urls import patterns, include, url
from inventory.urls import urlpatterns as inventory_url
from recipes.urls import urlpatterns as recipes_url
from users.urls import urlpatterns as user_url
from Measures.urls import urlpatterns as measures_url
from service.urls import urlpatterns as service_url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(user_url)),
    url(r'^inventory/', include(inventory_url)),
    url(r'^recipes/', include(recipes_url)),
    url(r'^measures/', include(measures_url)),
    url(r'^service/', include(service_url)),
)
