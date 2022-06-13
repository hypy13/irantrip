from django.contrib.auth.backends import BaseBackend

from apps.account.models import User


class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number, password, **kwargs):
        """
            authenticate user using phone_number
        """
        if user := User.objects.filter(phone_number=phone_number).first():
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None

    @staticmethod
    def user_can_authenticate(user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, 'is_active', True)
