from djorm_pgfulltext.models import SearchManagerMixIn 
from django.contrib.gis.db.models import GeoManager
#import djorm_pgfulltext.models 

class GeoFullTextManager(SearchManagerMixIn, GeoManager):
	'''A controller that allows for both GIS and Full Text'''
	pass
