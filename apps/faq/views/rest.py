from ..serializer import FaqListSerializer
from rest_framework.generics import ListAPIView
from ..settings import FAQ_ENABLE_MULTILINGUAL
from ..models import Faq


class FaqListView(ListAPIView):
    serializer_class = FaqListSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Faq.objects.filter(status=True).order_by('priority')

        if FAQ_ENABLE_MULTILINGUAL:
            qs = qs.filter(language__code=self.request.LANGUAGE_CODE)

        return qs
