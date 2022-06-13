from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('_message', 'user', 'created_at', 'status')
    readonly_fields = ('user', 'status')
    actions = ['approve_comments']

    @admin.display
    def _message(self, obj: Comment):
        return obj.message[:10] + ' ...'

    def has_add_permission(self, request):
        return True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.content_type = self.get_for_model()
        return super().save_model(request, obj, form, change)

    def approve_comments(self, request, queryset):
        queryset.update(status='approved')

    def get_for_model(self):
        """
            :return the model that this comment should belongs to
        """
        return ContentType.objects.get(model=self.model._meta.model_name)
