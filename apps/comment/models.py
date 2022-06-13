import re

import emoji
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class CommentManager(models.Manager):
    def all_approved(self):
        qs = super().filter(parent=None, status='approved')
        return qs


class Comment(MPTTModel):
    class CommentStatus(models.IntegerChoices):
        approved = 1, _('Approved')
        rejected = 2, _('Rejected')
        pending = 3, _('Pending')

    message = models.TextField(verbose_name=_('message'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    user = models.ForeignKey(
        verbose_name=_('user'), to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    name = models.CharField(max_length=119, null=True, blank=True, verbose_name=_('name'))
    is_insta = models.BooleanField(default=False, verbose_name=_('Is Instagram Comment'))
    phonenumber = models.CharField(max_length=119, null=True, blank=True, verbose_name=_('phonenumber'))
    like_count = models.PositiveIntegerField(verbose_name=_('likes count'), default=0)
    commentable_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    commentable = GenericForeignKey('content_type', 'commentable_id')
    status = models.PositiveSmallIntegerField(
        verbose_name=_('status'), choices=CommentStatus.choices, default=CommentStatus.pending
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    rate = models.PositiveSmallIntegerField(default=5, verbose_name=_('rate'))
    is_reaction = models.BooleanField(default=False, verbose_name=_('is reaction'))

    objects = CommentManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")

    def children(self):
        return Comment.objects.filter(parent=self, status='approved')

    @property
    def is_parent(self):
        return True if self.parent else False

    def __str__(self):
        return "%s. %s ..." % (self.pk, self.message[:13])

    def save(self, *args, **kwargs):
        def is_emoji(txt):
            txt = emoji.replace_emoji('زیبا و خاص😍😍🔥🔥', replace='')
            if len(txt) > 1:
                return False
            return True

        self.is_reaction = is_emoji(re.sub(r'@\w+', '', self.message, 1))
        super(Comment, self).save(*args, **kwargs)
