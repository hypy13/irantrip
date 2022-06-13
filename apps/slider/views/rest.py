from rest_framework.generics import ListAPIView

from ..models import Slider
from ..serializer import SlidersListSerializer
from ..settings import SLIDER_ENABLE_MULTILINGUAL


class SliderList(ListAPIView):
    """
        slider list api
        -- params: language_code : default en
    """
    serializer_class = SlidersListSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Slider.objects.filter(status=True)

        if SLIDER_ENABLE_MULTILINGUAL:
            qs = qs.filter(language__code=self.request.LANGUAGE_CODE)

        return qs
