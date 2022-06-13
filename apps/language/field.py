from django.db import models
from django.utils.translation import gettext_lazy as _


class LanguageField(models.ForeignKey):
    def __init__(self, limit_choices_to=None, related_name=None, **kwargs):
        kwargs.setdefault('limit_choices_to', limit_choices_to or {'status': True})
        kwargs.setdefault('related_name', related_name or "+")
        kwargs.setdefault('verbose_name', _('language'))
        kwargs.setdefault('on_delete', models.PROTECT)
        kwargs.setdefault('to', "language.Language")
        kwargs.setdefault('default', 69)

        super().__init__(
            **kwargs
        )
