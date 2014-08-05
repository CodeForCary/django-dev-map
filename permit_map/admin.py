from django.contrib.gis import admin 
from models import Permit

# One of the great things about using django. This line of code adds the 
# ability to see all of our permit regions in the admin interface. And 
# edit them, if we were so inclined.
admin.site.register(Permit, admin.GeoModelAdmin)
