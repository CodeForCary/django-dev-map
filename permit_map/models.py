# We use the GeoManager as the main object manager for Permit
from django.contrib.gis.db.models import GeoManager
# We use the SearchManager as a secondary manager
from djorm_pgfulltext.models import SearchManager
# Other imports required by these managers are:
from djorm_pgfulltext.fields import VectorField
from django.contrib.gis.db import models


class Permit(models.Model):
	'''Stores information about a single permit'''
	# The region field stores the geometric shape(s) of the permit
	region = models.MultiPolygonField(srid=4326, null=True)

	# All of these are non-required fields pulled from KML data
	name = models.CharField(max_length=1024, null=True)
	comment = models.CharField(max_length=1024, null=True)
	category = models.CharField(max_length=1024, null=True)
	proj_id = models.CharField(max_length=1024, null=True)
	link = models.CharField(max_length=1024, null=True)
	status = models.CharField(max_length=1024, null=True)
	description = models.TextField(null=True)

	# This manager is what allows us to make GIS queries (such as 
	# contains, overlap, bbcontains, etc.). It must be the main 
	# manager on this model type or we cannot make these queries.
	objects = GeoManager()

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
		fields = ('name', 'comment', 'category', 'proj_id', 'link', 'status'), 
		# This may be redundant now. 
		auto_update_search_field = False
	)

	def to_small_dict(self):
		'''Return a subset of the data useful for display in the UI.'''
		centroid = self.region.centroid
		return {
			'centroid': [ centroid.y, centroid.x ],
			'category': self.category,
			'comment': self.comment,
			'proj_id': self.proj_id,
			'status': self.status,
			'name': self.name,
			'link': self.link,
			'id': self.id
		}

	def __str__(self):
		return self.name
