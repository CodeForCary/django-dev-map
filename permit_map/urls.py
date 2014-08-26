from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.conf.urls import include, url
from django.contrib import admin

from permit_map import models
from permit_map import views

urlpatterns = [
	# This URL maps to / and is the main UI render. Note that we just spit out the contents of the permit_map/index.html template.
	url(r'^$', TemplateView.as_view(template_name="permit_map/index.html"), name='map'),
	# Lots of things going on here:
	# - We're using a open source view to render our permits into geoJSON because our view is quite simple. If we had 
	#   more complex view data, we could customize it, but this is more than enough for now.
	# - We're caching the results of this view for one month. This will also cause the page to be rendered using HTTP
	#   headers that cause it to be cached in the user's browser. See the cache_page docs for more.
	url(r'^permits/geojson', cache_page(2592000)(GeoJSONLayerView.as_view(model=models.PermitArea, geometry_field='region', 
		properties=['category', 'id', 'township'])), name='geojson'),
	# Full text search entry point, delegates to views.search (views.py)
	# Permit lookup point, delegates to views.permitsat (views.py)
	url(r'^search', views.search, name='search'),
	url(r'^permitsat', views.permitsat, name='permitsat')
]
