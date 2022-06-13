from rest_framework import serializers
from .models import Faq


class FaqListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ('question', 'answer',)
