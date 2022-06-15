from .base import *
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://ivi3.ir',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 5000,
    }
}

# sentry_sdk.init(
#     dsn="https://9d30e377eebe4fbc8805bfb8f366a9b9@o1127298.ingest.sentry.io/6169753",
#     integrations=[DjangoIntegration()],
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
#
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
#     'rest_framework.renderers.JSONRenderer',
# ]
