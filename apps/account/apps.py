from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = 'apps.account'
    icon = 'icon-users'
    verbose_name = _("Users")

