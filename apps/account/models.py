from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.contrib.auth.models import _user_has_perm, AbstractUser  # type: ignore
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.account.validators import validate_possible_number
from random import randint
import datetime


class UserManager(BaseUserManager):
    def create_user(
            self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(AbstractUser):
    first_name = models.CharField(verbose_name=_('first name'), max_length=254, null=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=254, null=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone_number = PhoneNumberField(
        verbose_name=_('phone number'), null=True, blank=True, unique=True, max_length=254, validators=[
            validate_possible_number
        ])
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("date joined"))
    avatar = models.FileField(verbose_name=_('avatar'), null=True, blank=True)

    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def is_guest(self):
        return self.email and len(self.email)

    class Meta:
        ordering = ("-id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users_user"

    def avatar_thumb(self):
        if self.avatar:
            return self.avatar.url


class VerificationCode(models.Model):
    phonenumber = models.CharField(max_length=90, validators=[validate_possible_number])
    code = models.PositiveSmallIntegerField()
    expire_at = models.DateTimeField()

    def __str__(self):
        return str(self.code)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.code = randint(1000, 9999)
        self.expire_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
        return super(VerificationCode, self).save(force_insert, force_update, using, update_fields)


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, verbose_name=_('fullname'))
    phonenumber = models.CharField(max_length=200, verbose_name=_('phonenumber'))
    state = models.CharField(max_length=200, verbose_name=_('state'))
    city = models.CharField(max_length=200, verbose_name=_('city'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    postal_code = models.CharField(max_length=200, verbose_name=_('postal code'))

    def __str__(self):
        return self.postal_code


class AdminUser(User):
    class Meta:
        ordering = ("email",)
        proxy = True
        verbose_name = _("Admin")
        verbose_name_plural = _('Admins')
