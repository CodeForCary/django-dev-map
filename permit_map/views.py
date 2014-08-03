from djgeojson.serializers import Serializer as GeoJSONSerializer
from djgeojson.http import HttpJSONResponse
from django.contrib.gis.geos import Point
from django.shortcuts import render
from django.http import HttpResponse
from models import Permit
import json

def search(request):
	response = '[]'
	if 'q' in request.GET:
		query = request.GET['q']
		if query:
			permits = Permit.text.search(query)
			response = json.dumps([ p.to_small_dict() for p in permits ])
	return HttpResponse(response, content_type='application/json')

def permitsat(request):
	response = '[]'
	if 'lat' in request.GET and 'lon' in request.GET:
		lon = request.GET['lon']
		lat = request.GET['lat']
		if lat and lon:
			permits = Permit.objects.filter(region__contains=Point(float(lon), float(lat)))
			response = json.dumps([ p.to_small_dict() for p in permits ])
	return HttpResponse(response, content_type='application/json')

#def geojson(request):
#	serializer = GeoJSONSerializer()
#	queryset = Permit.objects.all()
#	response = HttpJSONResponse()
#
#	serializer.serialize(queryset, stream=response, ensure_ascii=False, 
#		geometry_field='region', properties=['category', 'id']
#	)
#
#	return response
