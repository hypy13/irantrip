from django.views.generic import ListView, DetailView
from nwh_faq.models import Faq
from nwh_faq.settings import FAQ_ENABLE_MULTILINGUAL


class BaseFaqListView(ListView):
    template_name = 'faq.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        qs = Faq.objects.filter(status=True)

        if FAQ_ENABLE_MULTILINGUAL:
            lang_code = self.request.LANGUAGE_CODE
            qs = qs.filter(language__code=lang_code)

        return qs
