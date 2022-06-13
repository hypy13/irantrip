from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FaqConfig(AppConfig):
    name = 'apps.faq'
    icon = 'icon-question3'
    verbose_name = _('FAQ')
