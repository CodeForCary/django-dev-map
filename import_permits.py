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

args = parser.parse_args()
for kml_file in args.files:
	import_file(kml_file)
