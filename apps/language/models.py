from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    code = models.CharField(max_length=2, unique=True, verbose_name=_('code'))
    status = models.BooleanField(default=False, verbose_name=_('status'))
    countries = models.JSONField(verbose_name=_('countries'))

    def __str__(self):
        return self.name
