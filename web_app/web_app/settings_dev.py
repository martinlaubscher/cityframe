from .settings import *

DEBUG = True

INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')

# add by frontend for testing to facilitate real-time visualization
# of changes made to the frontend code.
CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173',
    'http://127.0.0.1:8000',
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
