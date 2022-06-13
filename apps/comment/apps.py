from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentConfig(AppConfig):
    name = 'apps.comment'
    icon = 'icon-city'
    verbose_name = _('comments')
