from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.conf.urls import include, url
from django.contrib import admin

from permit_map import models
from permit_map import views

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name="permit_map/index.html"), name='map'),
	url(r'^permits/geojson', cache_page(None)(GeoJSONLayerView.as_view(model=models.Permit, geometry_field='region', properties=['category', 'id'])), name='geojson'),
	#url(r'^permits/geojson', views.geojson, name='geojson'),
	url(r'^search', views.search, name='search'),
	url(r'^permitsat', views.permitsat, name='permitsat')
]
