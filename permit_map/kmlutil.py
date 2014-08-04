from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis import geos
from django.core.cache import cache
from shapely.ops import transform
from bs4 import BeautifulSoup
from functools import reduce
from models import Permit
from fastkml import kml

DEFAULT_FOLDERS = [
	'Site/Sub Plan',
	'Rezoning Case',
	'Development'
]
def placemark_generator(data, folders=DEFAULT_FOLDERS, name=None):
	'''A generator method that recursively descends through a fastkml 
	document and extracts Placemark objects from the KML document. 
        This method also returns the name of the Folder containing the 
        placemark. If the name is not in the provided folder white list, 
	it is skipped. The yielded value is (placemark, name).'''
	for feature in data.features():
		if isinstance(feature, kml.Placemark):
			if name in folders:
				yield (feature, name)
		else:
			if isinstance(feature, kml.Folder):
				name=feature.name
			for obj in placemark_generator(feature, folders=folders, name=name):
				yield obj 
DATA_TRANSFORMS = [
	lambda line : line.replace('xsd:', ''),
	lambda line : line.replace('gx:', '')
]
def parse_kml_file(path):
	'''Open the provided file, massage its contents, and parse with fastkml.'''
	with open(path, 'r') as kml_file:
		# This little turn of python will use a functional reduction to
		# apply each function in the DATA_TRANSFORMS array to the input 
		# file. So the file data passes through the functions in the D_T 
		# array as a chain: D_T[LEN](DT[LEN-1}(...)). It is designed 
		# this way so that as we find more erros in the KML formatting, 
		# we can add in additional preprocessors.
		kml_data = reduce((lambda x, y: y(x)), DATA_TRANSFORMS, kml_file.read())
	obj = kml.KML()
	obj.from_string(kml_data)
	return obj

def import_file(path):
	'''Import the KML at the specified path.'''
	import_fastkml_doc(parse_kml_file(path))

def import_fastkml_doc(doc):
	'''Import the provided fastkml document.'''
	# SIMPLIFY DESIGN FOR NOW. Add this code later if it makes sense.
	# We do a lot of damage in one line here. We create a generator for our
	# KML object that gives us each Placemark in the KML file as a tuple. 
	# As we pull from that generator, we sort the list descending in area. 
	# This is done in the hopes that our overlap detection logic below will
	# have less work to do.
	# tuples = sorted(placemark_generator(doc), key=(lambda p : -p[0].geometry.area))
	#for t in tuples: # loop over each placemark tuple
	# SIMPLIFY DESIGN FOR NOW. Add this code later if it makes sense.

	for t in placemark_generator(doc): # loop over our tuple generator
		placemark = t[0] # generator puts the placemark in t[0]
		category = t[1]  # and the category goes into t[1]

		# The KML data from the township includes Z coordinates in the 
		# lat/long, but the Z coord is always 0. The database cannot 
		# store the Z coord as configured, and it's worthless data 
		# anyway. Use the transform function to strip out Z.
		geom2d = transform((lambda x, y, z : filter(None, tuple([x, y, None]))), placemark.geometry)
		# Now we can convert the shapely geometry into a django geometry...
		geom = GEOSGeometry(geom2d.wkt, srid=4326) 
		# The town data mixes Polygons and MultiPolygons in their data.
		# That's fine, and we could eventually have a model that stores
		# one or the other. For the moment, however, it's much easier 
		# to convert all Polygons to MultiPolygons.
		if geom and isinstance(geom, geos.Polygon):
			geom = geos.MultiPolygon(geom)

		# Create a django model object with the geometry and the description
		permit = Permit(region=geom, description=placemark.description)

		# Use a helper method to extract all the data we can find fro mthis 
		# placemark as individual fields (instead of HTML formatted text).
		fields = extract_fields(placemark)
		for field, value in extract_fields(placemark).iteritems():
			# Use python's reflection abilities to set the field
			setattr(permit, field, value)

		# Save the record to the database. Note that we're not doing any 
		# de-duplication here because it's really difficult to tell when 
		# data is being added. Sometimes we get a new record for a region 
		# or a sub/super-region with useful comments. Rather than throwing
		# that away, store everything and make it all visible to the user.
		permit.save()


	# Manually update full text search after all imports are complete
	Permit.text.update_search_field()

	# Manually clear django's caches to serve new data
	cache.clear()

def extract_fields(placemark):
	'''Attempts to extract field infromation based on the format of the files we've seen so far.'''
	try:
		return extract_extdata(placemark)
	except AttributeError:
		return extract_xml(placemark)

EXT_DATA_TO_FIELD_MAPPING = {
	'ProjectName': 'name',
	'Comments': 'comment',
	'Type': 'category',
	'ID': 'proj_id',
	'Link': 'link',
}
def extract_extdata(placemark):
	'''Town of Cary stores fields in the ExtendedData field. Extract using fastkml'''
	result = {}
	# This reads out the map data as an array of dictionaires with the keys 'name' and
	# 'value'. Map those field names into our internal format.
	extdata = placemark.extended_data.elements[0].data
	for entry in extdata:
		key = entry['name'] # figure out the key name
		# If it's a key that we recognize, add the value to the result set with 
		# the sanatized key name.
		if key in EXT_DATA_TO_FIELD_MAPPING:
			result[EXT_DATA_TO_FIELD_MAPPING[key]] = entry['value']
	return result

XML_DATA_TO_FIELD_MAPPING = {
	'More_Info': 'link',
	'Type': 'category',
	'Status': 'status',
	'FID': 'proj_id',
	'Name': 'name'
}
def extract_xml(placemark):
	'''Apex only provides HTML description data at the moment. Parse it out.'''
	xml = BeautifulSoup(placemark.description) # Not strict XML, use HTML parser
	result = {}
	# The data is stored as rows in a nested table. Get the rows from that table
	for tr in xml.find_all('table')[1].find_all('tr'): 
		td = tr.find_all('td') # Get the fields
		if len(td) == 2:
			key = td[0].get_text() # field name is in the first td
			if key in XML_DATA_TO_FIELD_MAPPING:
				# Use the key name to pivot on our map above
				result[XML_DATA_TO_FIELD_MAPPING[key]] = td[1].get_text()
	return result
