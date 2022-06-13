from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactUs(models.Model):
    class ContactUsStatus(models.TextChoices):
        unread = ('unread', _('unread'))
        read = ('read', _('read'))
        answered = ('answered', _('answered'))

    name = models.CharField(verbose_name=_('name'), max_length=128)
    email = models.EmailField(verbose_name=_('email'), null=True, blank=True)
    message = models.TextField(verbose_name=_('message'))
    phone_number = models.CharField(verbose_name=_('phone number'), max_length=128, blank=True, null=True)
    answer = models.TextField(
        verbose_name=_('answer'),
        null=True, blank=True, help_text=_('this text will send by email to user if email is filled')
    )

    status = models.CharField(
        verbose_name=_('status'), max_length=8, choices=ContactUsStatus.choices,
        default=ContactUsStatus.unread
    )
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)

    def __str__(self):
        return self.message[:17] + ' ...'

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('contact-us')
        verbose_name_plural = _("contact-us messages")
