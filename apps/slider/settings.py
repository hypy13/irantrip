from django.conf import settings

SLIDER_ENABLE_MULTILINGUAL = \
    getattr(settings, 'ALL_MULTILINGUAL') or getattr(settings, 'SLIDER_ENABLE_MULTILINGUAL') or False

SLIDER_APP_ICON = getattr(settings, 'SLIDER_APP_ICON', 'icon-images2')

SLIDER_ABSTRACT_MODEL = getattr(settings, 'SLIDER_ABSTRACT_MODEL', False)
