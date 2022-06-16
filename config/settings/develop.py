from .base import *

CORS_ALLOW_ALL_ORIGINS = True
DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
