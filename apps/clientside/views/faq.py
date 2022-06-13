from nwh_faq.views.temp import BaseFaqListView


class FaqView(BaseFaqListView):
    template_name = 'front/pages/faq.html'
