from django.conf import settings

CONTACTUS_APP_ICON = getattr(settings, 'CONTACTUS_APP_ICON', 'mi-contact-mail')

CONTACTUS_ENABLE_ABSTRACTION = getattr(settings, 'CONTACTUS_ENABLE_ABSTRACTION', False)
