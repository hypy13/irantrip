from rest_framework.generics import ListAPIView

from .models import Language
from .serializer import LanguageSerializer


class LanguageList(ListAPIView):
    """
        language list api
    """
    pagination_class = None
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.filter(status=True)
