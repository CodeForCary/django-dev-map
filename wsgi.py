#!/usr/bin/python
import sys
import os

# Setup the WSGI (HTTP) handler for OpenShift. Ignore if not using OpenShift.

# Add the django cfac app to the environemnt
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR']))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cfac.settings'

# Establish our Python virtualenv -- loads necessary deps
virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

# Hook django into the WSGI handler
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
