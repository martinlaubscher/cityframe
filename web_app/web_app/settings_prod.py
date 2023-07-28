from .settings import *

DEBUG = False

INSTALLED_APPS = INSTALLED_APPS
MIDDLEWARE = MIDDLEWARE

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
