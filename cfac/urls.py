from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cfac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Map the permit app to the root of the site
    url(r'^', include('permit_map.urls', namespace='permit_map')),
    url(r'^admin/', include(admin.site.urls)),
)
