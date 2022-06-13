from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.post.models import LanguageField


class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    photo = models.ImageField(upload_to='media/sliders')
    status = models.BooleanField(default=True, verbose_name=_('status'))
    language = LanguageField()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['id']
