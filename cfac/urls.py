from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# This is the main routing table for our Django application. All non-static 
# requests come through here. At the moment we are routing / into the permit
# application. See permit_map/urls.py for the URLs supported by that app.
urlpatterns = patterns('',
    url(r'^', include('permit_map.urls', namespace='permit_map')),
    url(r'^admin/', include(admin.site.urls)),
)
