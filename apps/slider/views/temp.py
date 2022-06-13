from django.views.generic import ListView

from apps.slider.models import Slider


class BaseFaqListView(ListView):
    template_name = 'slider.html'
    context_object_name = 'sliders'

    def get_queryset(self):
        return Slider.objects.filter(status=True)
