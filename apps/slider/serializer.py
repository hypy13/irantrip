from rest_framework import serializers
from .models import Slider

from dj_filer.admin import get_thumbs


# Serializers define the API representation.
class SlidersListSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.SerializerMethodField('get_photo_object')

    class Meta:
        model = Slider
        fields = ('title', 'photo')

    def get_photo_object(self, obj: Slider):
        return get_thumbs(obj.photo, self.context.get('request'))
