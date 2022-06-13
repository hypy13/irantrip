from categories.models import Category
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.comment.models import Comment
from apps.tour.fields.summernote import SummernoteField
from config.settings.base import LANGUAGE_CHOICES


class Post(models.Model):
    class Status(models.IntegerChoices):
        draft = (0, 'Draft')
        publish = (1, 'Publish')

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    photo = models.ImageField(upload_to='blogs')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = SummernoteField(verbose_name=_('content'))
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.draft)
    categories = models.ManyToManyField(
        "categories.Category", related_name='posts', blank=True, verbose_name=_('categories')
    )
    tags = TaggableManager(blank=True, verbose_name=_('tags'))

    def summary(self):
        return self.textify(self.content)[:120] + ' ...'

    def comments(self):
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            commentable_id=self.id,
            level=0,
        ).all()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def textify(self, html):
        import re
        from django.utils.html import strip_tags
        # Remove html tags and continuous whitespaces
        text_only = re.sub('[ \t]+', ' ', strip_tags(html))
        # Strip single spaces in the beginning of each line
        return text_only.replace('\n ', '\n').strip()


class LanguageField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        super(LanguageField, self).__init__(
            max_length=2, choices=LANGUAGE_CHOICES, default='en', verbose_name=_('language'),
        )


LanguageField().contribute_to_class(Category, 'language')

from categories.admin import CategoryAdmin

CategoryAdmin.fieldsets = fieldsets = (
    (None, {
        'fields': ('language', 'parent', 'name', 'thumbnail', 'active')
    }),
    (_('Meta Data'), {
        'fields': ('alternate_title', 'alternate_url', 'description',
                   'meta_keywords', 'meta_extra'),
        'classes': ('collapse',),
    }),
    (_('Advanced'), {
        'fields': ('order', 'slug'),
        'classes': ('collapse',),
    }),
)
