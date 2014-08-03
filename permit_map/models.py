from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from django.contrib.gis.db import models

#import managers
from django.contrib.gis.db.models import GeoManager

# Create your models here.
class Permit(models.Model):
	#category = models.CharField(max_length=1024)
	region = models.MultiPolygonField(srid=4326, null=True)

	name = models.CharField(max_length=1024, null=True)
	comment = models.CharField(max_length=1024, null=True)
	category = models.CharField(max_length=1024) #, null=True)
	proj_id = models.CharField(max_length=1024, null=True)
	link = models.CharField(max_length=1024, null=True)
	status = models.CharField(max_length=1024, null=True)

	description = models.TextField(null=True)

	objects = GeoManager()

	search_index = VectorField()
	text = SearchManager(
		fields = ('name', 'comment', 'category', 'proj_id', 'link', 'status'), 
		auto_update_search_field = False
	)

	def to_small_dict(self):
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
		return self.category
#
#	class Meta:
#		# TODO kendm: REMOVE THIS HACK
#		app_label = 'permit_map'
