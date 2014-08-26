#!/usr/bin/python

import argparse
import os

# First, establish our django environment. This script is very specific to our 
# applicaiton, so I see no reason to make this command line configurable. Easy
# enough to do later if it becomes necessary.
os.environ['DJANGO_SETTINGS_MODULE'] = 'cfac.settings'
from django.conf import settings
from permit_map.models import CARY, APEX

# Use standard python conventions for parsing command line arguments.
parser = argparse.ArgumentParser(description='Import permit KML into database')
parser.add_argument('files', type=str, nargs='+',
	help='KML files for import')
parser.add_argument('--truncate', action='store_true',
	help='Clear the database before importing')
parser.add_argument('--town', action='store', required=True,
	choices=[ CARY, APEX ],
	help='The name of the town the file came from')

# Parse the command line into the args object
args = parser.parse_args()

if args.truncate:
	print 'Truncating Permit data.'
	from permit_map.models import PermitData, PermitArea
	PermitData.objects.all().delete()
	PermitArea.objects.all().delete()

from permit_map.shapeutil import CaryGenerator
PROCESSORS = {
	CARY: CaryGenerator
}

for kml_file in args.files:
	print "Importing %s permit file: %s"%(args.town, kml_file)
	PROCESSORS[args.town].load(kml_file)
