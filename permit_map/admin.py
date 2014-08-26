from models import PermitArea, PermitData
from django.contrib.gis import admin 

# One of the great things about using django. This line of code adds the 
# ability to see all of our permit regions in the admin interface. And 
# edit them, if we were so inclined.
admin.site.register(PermitArea, admin.GeoModelAdmin)
admin.site.register(PermitData, admin.GeoModelAdmin)
