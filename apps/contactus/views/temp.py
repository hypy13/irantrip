from django.views.generic import FormView
from nwh_contactus.models import ContactUs
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'phone_number', 'email', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Full Name')}),
            'phone_number': forms.NumberInput(attrs={'placeholder': _('Phone Number')}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'message': forms.Textarea(attrs={'placeholder': _('Message')}),
        }


class BaseContatctUsView(FormView):
    template_name = 'contactus.html'
    form_class = ContactUsForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Thank you for getting in touch! We appreciate you contacting us'))
        return super(BaseContatctUsView, self).form_valid(form)
