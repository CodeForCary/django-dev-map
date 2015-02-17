from django.contrib.gis.geos import GEOSGeometry
from models import PermitArea, PermitData
from django.contrib.gis import geos
from django.core.cache import cache
from shapely.ops import transform
from bs4 import BeautifulSoup
from datetime import date
from fastkml import kml

from datetime import datetime 
from datetime import date
from os import path
import re

from permit_map.models import SITE_SUBPLAN, REZONE 

# file -> (category, geom, data_dict) -> include?(data_dict) -> PermitArea -> PermitData

class PermitGenerator(object):
	'''Base logic for all permit producers'''
	def __init__(self, township, usedate):
		# All data sources need to have township and date info passed in
		self.township = township
		self.usedate = usedate


	def records(self):
		'''Return generator over all permits that yields the tuple (category, geom, data_dict)'''
		# Subclasses have to implement this!
		pass

	def process(self):
		for record in self.records():
			category = record[0] # our category is first in the tuple
			geom = fix_polygon(record[1]) # the region is next
			data_dict = record[2] # dict of field is next

			# Convert the shapely geometry into a django geometry...
			geom = GEOSGeometry(geom.wkt, srid=4326) # 4326 is standard lat/lng projection
			# The towns data mixes Polygons and MultiPolygons in their data.
			# That's fine, and we could eventually have a model that stores
			# one or the other. For the moment, however, it's much easier 
			# to convert all Polygons to MultiPolygons.
			if geom and isinstance(geom, geos.Polygon):
				geom = geos.MultiPolygon(geom)

			permit = None # This is our PermitArea object. Either find a duplicate or create a new one

			# This little query finds all regions currently in the database that intersect with 
			# our region. It also calculates those intersections as geometries. We're going to 
			# use this to de-duplicate on region.
			for overlap in PermitArea.objects.filter(region__intersects=geom).intersection(geom):
				intersect = overlap.intersection # calculated intersection area
				# First test: Do they overlap by at least 98%?
				if intersect.area > 0 and geom.area / intersect.area > 0.98:
					# Second test: Do the two regions have almost identical areas? If so, they must be the same
					if abs((overlap.region.area - geom.area) / ((overlap.region.area + geom.area) / 2)) < 0.02:
						# If there's more than one match (unlikely?) pick the one with the max intersection
						if permit is None or intersect.area > permit.intersection.area:
							permit = overlap

			if permit is None: # There's no duplicates. Create a PermitArea for our geom!
				permit = PermitArea(region=geom, first_seen=self.usedate, township=self.township)

			# Always update the category and the last-seen time
			permit.last_seen = self.usedate
			permit.category = category

			# Save our permit area.
			permit.save()

			# At the moment, all of our types use PermitData. If they stop using PermitData,
			# we'll have to delegate this logic to the subclass. This logic sucks, but what 
			# we're doing is finding out if we already have this VALUE for this region. If 
			# we do, then we don't store the value into this row. Therefore each row contains 
			# only unique, new values for this region.
			voided = 0 # If we void out all the data, then there's no point in saving the row
			for key, value in data_dict.iteritems():
				if PermitData.objects.filter(**{ key: value, 'owner': permit }).count() > 0:
					data_dict[key] = None
					voided += 1
			if voided != len(data_dict):
				data_dict['saved_on'] = self.usedate
				data_dict['owner'] = permit
				PermitData(**data_dict).save()

	@classmethod
	def load(cls, shapefile, usedate=None):
		usedate = date_from_filename(shapefile) if usedate is None else usedate
		processor = cls(shapefile=shapefile, usedate=usedate)
		processor.process()

		# Calculate the search index
		PermitData.text.update_search_field()

		# Manually clear django's caches to serve new data
		cache.clear()

class KmlGenerator(PermitGenerator):
    def __init__(self, township, usedate, shapefile, catfilter):
        super(KmlGenerator, self).__init__(township, usedate)
        self.catfilter = catfilter
        self.shapefile = shapefile

    def extract_fields(self, placemark):
        return {}

    def get_category(self, data_dict):
        if 'category' in data_dict:
                category = data_dict['category']
                if category in self.catfilter or len(self.catfilter) == 0:
                        return category
        return None

    def data_generator(self, data):
        for feature in data.features():
            if isinstance(feature, kml.Placemark):
                data_dict = self.extract_fields(feature)
                category = self.get_category(data_dict)
                if category is not None:
                    yield (category, feature.geometry, data_dict)
            else:
                for obj in self.data_generator(feature):
                    yield obj

    def sanatize(self, kml_txt):
        return re.sub('(xsd|gx):', '', kml_txt)
    
    def records(self):
        with open(self.shapefile, 'r') as kml_file:
            kml_data = self.sanatize(kml_file.read())
            obj = kml.KML()
            obj.from_string(kml_data)
            for result in self.data_generator(obj):
                yield result

class CaryGenerator(KmlGenerator):
    def __init__(self, shapefile, usedate, mapping={ 'ProjectName': 'name', 'Comments': 
        'comment', 'Type': 'category', 'ID': 'proj_id', 'Link': 'link', }):
        super(CaryGenerator, self).__init__('Cary', usedate, shapefile, { 'Site/Sub Plan', 'Rezoning Case' })
        self.mapping = mapping

    def extract_fields(self, placemark):
        result = {}
        extdata = placemark.extended_data.elements[0].data
        for entry in extdata:
                key = entry['name'] # figure out the key name
                # If it's a key that we recognize, add the value to the result set with 
                # the sanatized key name.
                if key in self.mapping:
                        result[self.mapping[key]] = entry['value']
        return result

    def get_category(self, data_dict):
        if 'category' in data_dict:
		return {
			'Site/Sub Plan': SITE_SUBPLAN,
			'Rezoning Case': REZONE 
		}.get(data_dict['category'], None)
        return None

class ApexGenerator(KmlGenerator):
    def __init__(self, shapefile, usedate, mapping={ 'More_Info': 'link', 
        'Type': 'category', 'Status': 'status', 'FID': 'proj_id', 'Name': 'name' }):
        super(ApexGenerator, self).__init__('Apex', usedate, shapefile, { 'Residential', 'Non-Residential', 'Town of Apex', 'Mixed Use' })
        self.mapping = mapping

    def extract_fields(self, placemark):
	'''Apex only provides HTML description data at the moment. Parse it out.'''
	xml = BeautifulSoup(placemark.description) # Not strict XML, use HTML parser
	result = {}
	# The data is stored as rows in a nested table. Get the rows from that table
	for tr in xml.find_all('table')[1].find_all('tr'): 
		td = tr.find_all('td') # Get the fields (<td>=<td> pairs)
		if len(td) == 2: # if we have 2 tds
			key = td[0].get_text() # field name is in the first td
			if key in self.mapping:
				# Use the key name to pivot on our map above
				result[self.mapping[key]] = td[1].get_text()
	return result

    def get_category(self, data_dict):
	    raise Error('need to implement categories for Apex')


def fix_polygon(geom):
	'''Standardize Shapely polygon into 2d'''
	if geom.has_z:
		# The KML data from some towns includes Z coordinates in the 
		# lat/long, but the Z coord is always 0. The database cannot 
		# store the Z coord as configured, and it's worthless data 
		# anyway. Use the transform function to strip out Z.
		geom = transform(lambda x, y, z : filter(None, tuple([x, y, None])), geom)
	return geom

def map_field_data(data_obj, fields):
	'''Helper method for mapping from a dict into an object'''
	for field, value in fields:
		setattr(data_obj, field, value)

def date_from_filename(shapefile):
	fname = path.basename(shapefile)
	match = re.search('[0-9]{8}', fname)
	if match is not None:
		usedate = datetime.strptime(match.group(0), '%Y%m%d').date()
	else:
		usedate = date.today()
	return usedate
