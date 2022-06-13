from rest_framework import serializers
from apps.account.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'avatar',)
