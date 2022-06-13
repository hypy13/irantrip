from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactusConfig(AppConfig):
    name = 'apps.contactus'
    icon = 'mi-contact-mail'
    verbose_name = _('Contact us')
