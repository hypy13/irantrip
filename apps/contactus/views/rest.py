from rest_framework.generics import CreateAPIView
from ..serializer import ContactUsSerializer


class ContactUsView(CreateAPIView):
    serializer_class = ContactUsSerializer
