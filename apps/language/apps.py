from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LanguageConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.language'
    icon = 'mi-g-translate'
    verbose_name = _('Languages')
