# We use the GeoManager as the main object manager for Permit
from django.contrib.gis.db.models import GeoManager
# We use the SearchManager as a secondary manager
from djorm_pgfulltext.models import SearchManager
# Other imports required by these managers are:
from djorm_pgfulltext.fields import VectorField
from django.contrib.gis.db import models

CARY = 'Cary'
APEX = 'Apex'

SITE_SUBPLAN = 'subplan'
REZONE = 'rezone'

class PermitArea(models.Model):
	'''Stores information about a single permit'''
	# The region field stores the geometric shape(s) of the permit
	region = models.MultiPolygonField(srid=4326, blank=False)
	# We need the category in order to color the map
	#category = models.CharField(max_length=1024, blank=False)
	category = models.CharField(max_length=7, choices=((SITE_SUBPLAN, SITE_SUBPLAN), (REZONE, REZONE)), blank=False)
	# What township contains this region?
	township = models.CharField(max_length=4, choices=((CARY, CARY), (APEX, APEX)), blank=False)

	# Keep track of when we've seen this field
	first_seen = models.DateField()
	last_seen = models.DateField()

	# This manager is what allows us to make GIS queries (such as 
	# contains, overlap, bbcontains, etc.). It must be the main 
	# manager on this model type or we cannot make these queries.
	objects = GeoManager()

	def get_timeline_data(self):
		result = dict([ (field, []) for field in PermitData.VALUE_FIELDS ])
		for row in self.data.all().order_by('-saved_on'):
			for field in PermitData.VALUE_FIELDS:
				value = getattr(row, field)
				if value is not None:
					result[field].append({ 'value': value, 'date': row.saved_on.isoformat() })
		return result

	def to_dict(self):
		centroid = self.region.centroid
		return {
			'first_seen': self.first_seen.isoformat(),
			'last_seen': self.last_seen.isoformat(),
			'centroid': [ centroid.y, centroid.x ],
			'data': self.get_timeline_data(),
			'category': self.category,
			'township': self.township,
			'id': self.id
		}


class PermitData(models.Model):
	# Attach this PermitData object to a specific PermitArea object
	owner = models.ForeignKey(PermitArea, related_name='data')

	# These are basic fields supported by all the municipalities that we 
	# currently pull data from. They are all character fields.
	name = models.CharField(max_length=1024, null=True)
	proj_id = models.CharField(max_length=1024, null=True)
	link = models.CharField(max_length=1024, null=True)
	status = models.CharField(max_length=1024, null=True)
	comment = models.TextField(null=True)
	# We also store this here in case it changes over time.
	# Having it here also gives us full text search on category
	category = models.CharField(max_length=1024, null=True)

	# Date on which the values in this row were captured
	saved_on = models.DateField()

	# We must use a GeoManager because of our foreign key relation to the
	# PermitArea object. Otherwise we'll get errors.
	objects = GeoManager()

	VALUE_FIELDS = ('name', 'comment', 'proj_id', 'link', 'status', 'category')

	# In order to support full text search, we have a SECOND model 
	# that allows for that access pattern. Attempts to use the GIS
	# mixin that is available in the pgfulltext module failed 
	# miserably, so we go with this route for now. The main drawback 
	# is that we must manually update the search fields on save 
	# because this is not the default manager. That's not too terrible,
	# however, because we only ever save from one place inside kmlutils.py.
	search_index = VectorField()
	text = SearchManager(
		# List all the fields that you want indexed
		fields = VALUE_FIELDS, 
		# This may be redundant now. Not sure.
		auto_update_search_field = False
	)

	@classmethod
	def create_query_dict(cls, area, data_dict):
		for field in PermitData.VALUE_FIELDS:
			if field not in data_dict:
				data_dict[field] = None
		data_dict['owner'] = area
		return data_dict

class TimelineData(object):
	def __init__(self, value, date):
		self.value = value
		self.date = date
	def __eq__(self, other):
		return self.value == other.value and self.date == other.date
	def __str__(self):
		return "%s: %s"%(self.date, self.value)

