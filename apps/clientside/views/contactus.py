from nwh_contactus.views.temp import BaseContatctUsView
from django.urls import reverse


class ContactUsView(BaseContatctUsView):
    template_name = 'front/pages/contactus.html'

    def get_success_url(self):
        return reverse('contact-us')
