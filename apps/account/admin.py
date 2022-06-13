from ajaxdatatable.admin import AjaxDatatable
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.account.models import User, AdminUser


@admin.register(AdminUser)
class AdminsAdmin(UserAdmin, AjaxDatatable):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
    ordering = 'email',
    readonly_fields = ('date_joined', 'last_login',)
    exclude = ('password', 'user_permissions')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'avatar',)}),
        (_('Permissions'), {
            'fields': ('password', 'is_active', 'is_staff', 'is_superuser', 'groups',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change) -> None:
        obj.is_staff = 1
        super(AdminsAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super(AdminsAdmin, self).get_queryset(request).filter(is_staff=1)


@admin.register(User)
class UsersAdmin(UserAdmin, AjaxDatatable):
    list_display = ('phone_number', 'first_name', 'last_name', 'date_joined', 'last_login')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined', 'last_login',)
    exclude = ('password', 'user_permissions')
    list_filter = ('is_active',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    save_as_continue = True

    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'password')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Avatar'), {'fields': ('avatar',), 'classes': ('aside',)}),
    )

    def get_queryset(self, request):
        return super(UsersAdmin, self).get_queryset(request).filter(is_staff=False)
