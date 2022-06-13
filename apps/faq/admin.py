from django.contrib import admin, messages
from django.db.models import Case, Value, When, FloatField
from django.http import JsonResponse
from django.urls import path

from .models import Faq


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    change_list_template = 'admin/faq_change_form.html'
    exclude = ['priority']
    list_filter = ['status']

    ordering = ('-priority', 'id')

    def changelist_view(self, request, extra_context=None):
        i = self.get_changelist_instance(request)
        info = self.model._meta.app_label, self.model._meta.model_name
        extra_context = {
            'items': i.get_queryset(request),
            'change_link': f"admin:{info[0]}_{info[1]}_change",
        }
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('faq-sort', self.admin_site.admin_view(self.sortable), name='faq_sort')
        ]
        return urls

    @staticmethod
    def sortable(request):
        set_query = []
        for _id, value in request.POST.items():
            set_query += {
                When(id=_id, then=Value(value))
            }
        result = Faq.objects.update(
            priority=Case(
                *set_query,
                default='priority',
                output_field=FloatField()
            )
        )
        if not result:
            messages.add_message(request, messages.WARNING, 'error occurred!', extra_tags='danger')
            return JsonResponse({'success': False}, status=500, safe=False)

        return JsonResponse({'success': True}, status=200, safe=False)
