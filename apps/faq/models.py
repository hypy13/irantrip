from django.db import models
from django.utils.translation import gettext_lazy as _


class Faq(models.Model):
    question = models.CharField(verbose_name=_('question'), max_length=255)
    answer = models.TextField(verbose_name=_('answer'))
    priority = models.IntegerField(verbose_name=_('priority'), null=True, blank=True)
    status = models.BooleanField(verbose_name=_('status'), default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['priority', '-id']
        verbose_name = _('FAQ')
        verbose_name_plural = _("FAQs")
