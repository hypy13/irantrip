from django.contrib import admin
from .models import Language


@admin.action(description="enable selected languages")
def enable_languages(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description="disable selected languages")
def disable_languages(modeladmin, request, queryset):
    queryset.update(status=False)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')
    ordering = ('-status', 'name',)
    actions = [
        enable_languages,
        disable_languages
    ]
    list_filter = ('status',)
    search_fields = ('name', 'code')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
