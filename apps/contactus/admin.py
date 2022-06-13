from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.mail import send_mail
from . import settings
from ajaxdatatable.admin import AjaxDatatable


class ContactUsAdmin(AjaxDatatable):
    list_display = ('name', 'email', 'created_at', 'status')
    readonly_fields = ('name', 'email', 'phone_number', '_message', 'created_at',)
    exclude = ('status', 'message')
    list_filter = ('status',)
    fields = readonly_fields + ('answer',)

    @staticmethod
    def _message(obj):
        return format_html(obj.message)

    def has_add_permission(self, request):
        return False

    def fail_send_email_response(self, req, o):
        self.message_user(req, 'Email did not sent please try again', messages.ERROR, extra_tags='danger')
        return HttpResponseRedirect(req.path)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        ContactUs.objects.filter(id=object_id, status=ContactUs.ContactUsStatus.unread).update(
            status=ContactUs.ContactUsStatus.read
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        from django.conf import settings
        if obj.email:
            sending_result = send_mail(
                subject='Response to requested email',
                message=obj.answer,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email]
            )
            if not sending_result:
                admin.ModelAdmin.response_change = self.fail_send_email_response
            else:
                obj.status = 'answered'

        return super().save_model(request, obj, form, change)


if not settings.CONTACTUS_ENABLE_ABSTRACTION:
    from .models import ContactUs

    admin.site.register(ContactUs, ContactUsAdmin)
