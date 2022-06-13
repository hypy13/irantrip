from django.contrib.auth import authenticate, password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.account.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'first_name', 'last_name',)

    def validate(self, attrs: dict):
        if password := attrs['password']:
            password_validation.validate_password(password, self.instance)

        attrs["username"] = attrs['phone_number']

        return attrs


class UserLoginSerializer(serializers.Serializer):
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(
                request=self.context.get('request'),
                phone_number=phone_number, password=password
            )

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
