from django.contrib.gis import admin 
from models import Permit

admin.site.register(Permit, admin.GeoModelAdmin)
