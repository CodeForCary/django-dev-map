#!/usr/bin/python

import argparse
import os

# First, establish our django environment. This script is very specific to our 
# applicaiton, so I see no reason to make this command line configurable. Easy
# enough to do later if it becomes necessary.
os.environ['DJANGO_SETTINGS_MODULE'] = 'cfac.settings'
from django.conf import settings
from permit_map.kmlutil import import_file

# Use standard python conventions for parsing command line arguments.
parser = argparse.ArgumentParser(description='Import permit KML into database')
parser.add_argument('files', type=str, nargs='+',
	help='KML files for import')
parser.add_argument('--truncate', action='store_true',
	help='Clear the database before importing')

# Parse the command line into the args object
args = parser.parse_args()

if args.truncate:
	print 'Truncating the Permit table.'
	from permit_map.models import Permit
	Permit.objects.all().delete()

for kml_file in args.files:
	print "Importing %s"%kml_file
	import_file(kml_file)
