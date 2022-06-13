from django.views.generic.base import TemplateView

from apps.post.models import Post
from apps.slider.models import Slider
from apps.tour.models import Tour


class HomePage(TemplateView):
    template_name = "front/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            'sliders': Slider.objects.filter(status=True).all(),
            'featured_tours': Tour.objects.filter(status=True, as_featured=True)[:5],
            'posts': Post.objects.order_by('-id')[:4],
        }

    # def get_faqs(self):
    #     from nwh_faq.models import Faq
    #     qs = Faq.objects.filter(status=True)
    #     return qs.all()


class IranVisa(TemplateView):
    template_name = 'front/iran-visa.html'


class Services(TemplateView):
    template_name = 'front/services.html'


class About(TemplateView):
    template_name = 'front/about.html'
