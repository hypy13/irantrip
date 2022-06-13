from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from apps.tour.fields.comma_sep import CommaSepModelField
from apps.tour.fields.keyvalue_field import JsonKeyValueField
from django.conf import settings

from apps.tour.fields.summernote import SummernoteField


class TourDays(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    text = SummernoteField(verbose_name=_('text'))
    tour = models.ForeignKey("Tour", related_name="days", verbose_name=_('tour days'), on_delete=models.CASCADE, null=True)


class Tour(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    slug = models.SlugField(max_length=200, unique=True)

    content = SummernoteField(verbose_name=_('content'))
    rate = models.PositiveSmallIntegerField(default=5, verbose_name=_('rate'))
    group_max = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=7)

    geo_points = CommaSepModelField()
    services = CommaSepModelField(null=True, blank=True)
    age_range = models.CharField(verbose_name=_('age range'), help_text=_('eg. 18-50'), max_length=10)
    features = JsonKeyValueField(null=True, blank=True, default=dict)

    cancellation_rule = CommaSepModelField()

    categories = models.ManyToManyField('categories.Category', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.PositiveSmallIntegerField(verbose_name=_('priority'), null=True, blank=True)
    status = models.BooleanField(verbose_name=_('status'), default=True)

    as_featured = models.BooleanField(default=False, verbose_name=_('as featured tour'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['priority', '-id']
        verbose_name = _('Tour Package')
        verbose_name_plural = _("Tour Packages")

    def get_duration(self):
        return (self.end_date - self.start_date).days

    def get_generated_star(self):
        html = ""
        float_part = round((self.rate % 1) / 0.25)
        for i in range(round(self.rate)):
            html += f'<i class="elegant-icon icon_star"></i>'

        if float_part == 3:
            html += f'<i class="elegant-icon icon_star-half"></i>'
        elif float_part == 2:
            html += f'<i class="elegant-icon icon_star-half"></i>'
        elif float_part == 1:
            html += f'<i class="elegant-icon icon_star-half"></i>'

        return mark_safe(html)


class TourPhotos(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='tours')


class TourRegistrar(models.Model):
    class Status(models.TextChoices):
        pending = 'PE', 'pending'
        completed = 'CO', 'completed'
        canceled = 'CA', 'canceled'

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.pending)

    class Meta:
        ordering = ('-id',)


class TourMember(models.Model):
    class Gender(models.TextChoices):
        male = 'M', 'male'
        female = 'F', 'female'

    registrar = models.ForeignKey(TourRegistrar, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255)
    born_country = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=Gender.choices)

    passport_country = models.CharField(max_length=255)
    passport_code = models.CharField(max_length=255)
    passport_expired_at = models.CharField(max_length=255)
    passport_issue = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('tour member')
        verbose_name_plural = _('tour members')
        ordering = ('-id',)
