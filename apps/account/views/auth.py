from django.contrib.auth.hashers import make_password
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.account.serializers import UserSignupSerializer, UserLoginSerializer


def generate_login_token(user):
    token, created = Token.objects.update_or_create(user=user)
    return token.key


class LoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    renderer_classes = (renderers.BrowsableAPIRenderer,)


class SignupView(CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response({
            "token": generate_login_token(user),
        }, status=200)

    def perform_create(self, serializer: UserLoginSerializer):
        raw_password = serializer.validated_data.pop('password')

        return serializer.save(
            password=make_password(raw_password),
            is_active=False,  # wait for user to authorize his account by sms
        )
