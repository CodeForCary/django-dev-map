from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.contrib.gis.measure import Distance, D
from django.shortcuts import render_to_response
from djgeojson.http import HttpJSONResponse
from django.template import RequestContext
from django.contrib.gis.geos import Point
from models import PermitArea, PermitData
from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
from itertools import chain
import json

def index(request):
    return render_to_response('permit_map/index.html', {
        'centroid': PermitArea.objects.collect().centroid,
        'bounds': list(PermitArea.objects.extent())
    }, context_instance=RequestContext(request))

def search(request):
	'''Return the results of a full text search as JSON'''
	response = {}
	if 'q' in request.GET:
		query = request.GET['q']
		if query:
                        ids = PermitData.text.search(query).values_list('owner__id', flat=True)
                        if len(ids) > 0:
                            permits = PermitArea.objects.filter(id__in=list(ids))
                            bounds = permits.extent()
                        else:
                            permits = []
                            bounds = []

                        response['permits'] = [ p.to_dict() for p in permits ]
                        response['bounds'] = list(bounds)
#			permits = PermitData.text.search(query) # full text search in one line!
#			
#			# Get list of match ids
#			ids = permits.values_list('owner__id', flat=True)
#			if len(ids) > 0:
#				bounds = PermitArea.objects.filter(id__in=ids).extent()
#			else:
#				bounds = []
#
#			# convert each matching Permit into a small_dict and convert to JSON.
#			response['permits'] = [ p.to_dict() for p in permits ]
#			response['bounds'] = list(bounds)
	return HttpResponse(json.dumps(response), content_type='application/json')

def _decode_lat_lon(request):
	if 'lat' in request.GET and 'lon' in request.GET:
		lon = request.GET['lon']
		lat = request.GET['lat']
		if lat and lon:
                    return Point(float(lon), float(lat))
        return None

def permitsat(request):
	'''Return all permits active at a specific lat/lng'''
	response = {}
	if 'lat' in request.GET and 'lon' in request.GET:
		lon = request.GET['lon']
		lat = request.GET['lat']
		if lat and lon:
			# GIS query asking for all Permits with a region that contains the requested point
			permits = PermitArea.objects.filter(region__contains=Point(float(lon), float(lat)))
			# convert each matching Permit into a small_dict and convert to JSON.
			response['permits'] = [ p.to_dict() for p in permits ]
                        response['bounds'] = list(permits.extent())
	return HttpResponse(json.dumps(response), content_type='application/json')

def overview(request):
	'''Return basic information about the permit data that we have on file.'''
        permit_glom = PermitArea.objects.collect()

        # Decode the user's location (if available) and list everything in 3 miles
        centroid = _decode_lat_lon(request)
        closest =  []
        bounds = []
        if centroid is not None and permit_glom.envelope.contains(centroid):
            #closest = PermitArea.objects.distance(centroid).order_by('distance').first()
            closest = PermitArea.objects.filter(region__distance_lt=(centroid, D(mi=1))).distance(centroid).order_by('distance')
            bounds = list(closest.extent())

        dates = []
        for o in PermitArea.objects.values('first_seen', 'last_seen').distinct():
            dates.append(o['first_seen'])
            dates.append(o['last_seen'])
        dates = list(set(dates))

	response = {
		'categories': sorted(PermitArea.objects.values_list('category', flat=True).distinct()),
		'towns': sorted(PermitArea.objects.values_list('township', flat=True).distinct()),
                'closest': {
                    'permits': [ p.to_dict() for p in closest ],
                    'bounds': bounds
                },
		'dates': [ d.isoformat() for d in sorted(dates) ],
	}
	return HttpResponse(json.dumps(response), content_type='application/json')
