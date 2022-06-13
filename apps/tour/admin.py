from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from apps.tour.models import Tour, TourDays, TourPhotos


class DaysInline(admin.TabularInline):
    model = TourDays
    extra = 1


class TourPhotosAdmin(admin.TabularInline):
    model = TourPhotos
    extra = 1


@admin.action(description=_('Mark Tours as Featured'))
def mark_as_featured(modeladmin, request, queryset):
    queryset.update(as_featured=True)
    messages.success(request, _('Successfully Mark Tours as Featured'))


@admin.action(description=_('Remove Tours From featured'))
def mark_as_not_featured(modeladmin, request, queryset):
    queryset.update(as_featured=False)
    messages.success(request, _('Successfully Remove Tours from Featured'))


@admin.action(description=_('Mark tours as Active status'))
def activated(modeladmin, request, queryset):
    queryset.update(status=True)
    messages.success(request, _('Successfully Activated Tours Status'))


@admin.action(description=_('Mark tours as Deactivate status'))
def deactivate(modeladmin, request, queryset):
    queryset.update(status=False)
    messages.success(request, _('Successfully Deactivated Tours Status'))


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'status', 'as_featured', 'priority', 'id')
    exclude = ['priority', 'geo_points', 'cancellation_rule', 'services']
    search_fields = ('title', 'content', 'price')
    list_filter = ['status', 'categories']
    ordering = ('-priority', 'id')
    inlines = [
        DaysInline, TourPhotosAdmin
    ]
    actions = [
        mark_as_featured,
        activated,
        deactivate,
        mark_as_not_featured,
    ]
    # filter_vertical = ('categories',)
    filter_horizontal = ('categories',)
    prepopulated_fields = {'slug': ('title',)}
