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
# Needed by OpenShift
import urlparse
import random

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

# SECURITY WARNING: don't run with debug turned on in production!
TEMPLATE_DEBUG = 'OPENSHIFT_REPO_DIR' not in os.environ
DEBUG = TEMPLATE_DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # These are the default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Added so South can do table migrations
    'django.contrib.gis',
    # Supports easy rendering of GeoJSON
    'djgeojson',
    # Our actual application
    'permit_map',
    # Easier SQL migration
    'south',
    # Helpers for using AngularJS
    #'djangular'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cfac.urls'

WSGI_APPLICATION = 'cfac.wsgi.application'

# Database configuration. cfac requires PostGIS for spatial queries, 
# so we are locked into postgresql. When doing local development, 
# use a cfac user with the password cfac. When on OpenShift, we pull
# from the environment.
DATABASES = {}
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
    DATABASES['default'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
	'NAME': os.environ['OPENSHIFT_APP_NAME'],
	'USER': url.username,
	'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
	'HOST': 'localhost',
	'PASSWORD': 'cfac',
        'NAME': 'cfac',
	'USER': 'cfac'
    }
POSTGIS_VERSION=(2, 1)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cfac'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# TODO kendm: Needed for real server impl
if 'OPENSHIFT_REPO_DIR' in os.environ:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
