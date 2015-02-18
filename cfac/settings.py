"""
Django settings for cfac project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Added for OpenShift configutation
import urlparse # To parse postgres URL
import random # To generate key

# Don't use this value in production, it's visible on GitHub. Good enough for dev.
SECRET_KEY = 'qb5qjs!f56(x0z1ssrb4*hav(+)%d0%bpy&wy4)x==b@t&xv0e'
# Else, in dev. Turn on DEBUG which disables ALLOWED_HOSTS
ALLOWED_HOSTS = [] # Defined, but empty
TEMPLATE_DEBUG = True
DEBUG = True

# Application definition
INSTALLED_APPS = (
	# These are the default django apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# Add GIS capabilities to Django
	'django.contrib.gis',
	# Supports easy rendering of GeoJSON
	'djgeojson',
	# Our actual application
	'permit_map',
	# Easier SQL migration
	'south',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Defines the routes and URLs for our REST services
ROOT_URLCONF = 'cfac.urls'

# Default
WSGI_APPLICATION = 'cfac.wsgi.application'

# Database configuration. cfac requires GeoDjango, which must run on a 
# spatial database. According to what I've read, Postgres is the best 
# free platform for GIS queries. Mongo may also work. Feel free to try.
DATABASES = {} # Start as an empty dict. Add based on environment
# Obviously alter this to suit your local environment
DATABASES['default'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'PASSWORD': 'cfac',
        'NAME': 'cfac',
        'USER': 'cfac'
}

# Added due to problems where the postgis backend couldn't properly parse
# the version out of the database. Manually specified. Change if you're 
# using a different version of postgis.
POSTGIS_VERSION=(2, 1)

# Argh. We need a caching solution because generating the geoJSON data is 
# really expensive/slow. Originally I had used memcached and it had great 
# performance, but OpenShift does not support it as a default cartridge, 
# likely because it's difficult to properly secure (as I discovered).
#
# I then switched to django's memory cache, but that one is process 
# local and we can't clear it easily from import_permits.
#
# The final workable option is the file cache. It's easy to clear cross
# process and while it's not as fast as the memory cache, it is much 
# better than building the geoJSON data every time.
CACHES = {}
CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/cfac.cache'
}


# Internationalization has been left at the defaults.
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Serve from the /static/ URL in both production and developpment
STATIC_URL = '/static/'
