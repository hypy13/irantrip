import requests
from django import forms
from django.contrib import messages
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.core import validators
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from ratelimit.decorators import ratelimit

from apps.account.models import User, VerificationCode


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '09101112233', 'autocomplete': 'phonenumber'}),
        label='شماره همراه',
    )
    password = forms.CharField(
        label=_("پسورد"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[validators.MinLengthValidator(1)],
    )

    def clean_username(self):
        value = self.cleaned_data['username']
        return "+98" + value[1:]


class RegistrationForm(forms.Form):
    phonenumber = forms.CharField(
        widget=forms.TextInput(
            attrs={'autofocus': True, 'placeholder': '09101112233', 'autocomplete': 'phonenumber'}
        ),
        label='شماره همراه',
    )
    password = forms.CharField(
        label=_("پسورد"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[validators.MinLengthValidator(5)],
    )
    password_confirm = forms.CharField(
        label=_("کانفیرم پسورد"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[validators.MinLengthValidator(5)],
    )
    verify_code = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'کد چهار رقمی', }, ))

    def clean_phonenumber(self):
        val = self.cleaned_data['phonenumber']
        val = "+98" + val[1:]
        if User.objects.filter(phone_number=val).exists():
            self.add_error('phonenumber', 'شما قبلا در سایت ثبت نام نموده اید.')

        return val

    def clean_verify_code(self):
        import datetime
        code = self.cleaned_data['verify_code']
        code = VerificationCode.objects.filter(
            phonenumber=self.cleaned_data['phonenumber'],
            code=int(code),
            expire_at__gte=datetime.datetime.now()
        )
        if not code.exists():
            self.add_error('verify_code', 'کد اعتبار سنجی صحیح نمی باشد یا منقضی شده است.')

        return code


class LoginView(auth_views.LoginView):
    form_class = LoginForm

    def form_invalid(self, form):
        redirect_url = self.request.POST['from_url'] + '?login=0'
        return redirect(redirect_url)

    def get_success_url(self):
        from_url = self.request.POST['from_url']
        if from_url == '/' or from_url == '/accounts/logout/':
            return reverse('profile')

        return from_url


class RegisterView(FormView):
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        return redirect('login')

    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data['phonenumber'],
            phone_number=form.cleaned_data['phonenumber'],
        )
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)
        from_url = self.request.POST['from_url']

        if from_url == '/' or from_url == '/accounts/logout/':
            return redirect(reverse('profile') + '?new-member=1')

        return redirect(from_url)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return redirect(
            self.request.POST['from_url'] + '?register=0'
        )


class PasswordResetForm(forms.Form):
    phonenumber = forms.CharField(
        widget=forms.TextInput(
            attrs={'autofocus': True, 'placeholder': '09101112233', 'autocomplete': 'phonenumber'}
        ),
        label='شماره همراه',
        # validators=[validate_possible_number, ],
    )
    verfiycode = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'کد چهار رقمی', }))
    password = forms.CharField(
        label=_("پسورد"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[validators.MinLengthValidator(5)],
    )
    password_confirm = forms.CharField(
        label=_("کانفیرم پسورد"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[validators.MinLengthValidator(5)],
    )

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']
        phonenumber = "+98" + phonenumber[1:]
        return phonenumber

    def clean_verfiycode(self):
        import datetime
        code = self.cleaned_data['verfiycode']
        code = VerificationCode.objects.filter(
            phonenumber=self.cleaned_data['phonenumber'],
            code=int(code),
            expire_at__gte=datetime.datetime.now()
        )
        if not code.exists():
            self.add_error('verfiycode', 'کد اعتبار سنجی صحیح نمی باشد یا منقضی شده است.')

        return code


class PasswordResetView(FormView):
    template_name = 'registration/reset_password.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        user = User.objects.filter(username=form.cleaned_data['phonenumber']).first()
        user.set_password(form.cleaned_data['password'])
        login(self.request, user)
        self.request.session['logged_in'] = user.id
        return redirect(reverse('profile') + '?reset_password=1')


@ratelimit(key='ip', rate='1/15s', block=True)
def send_code(request):
    code = VerificationCode.objects.create(
        phonenumber=request.POST.get('number'),
    )

    url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
    res = requests.post(url, data={
        'username': '09338234779',
        'password': 'YZH$F',
        'to': code.phonenumber,
        'from': '50004001234779',
        'text': f' کد تایید عضویت شما در سایت آلاگالری : {code}'
    }).json()

    print(res)
    if res.get('RetStatus') == 1:
        return JsonResponse({
            'success': True,
            # 'message': code.code,
            'message': 'sent!',
        })
    elif res.get('Value') == '5':
        return JsonResponse({
            'success': False,
            'message': 'شماره هماره وارد شده صحیح نمی باشد . لطفا شماره همراه معتبر وارد کنید.'
        })
    else:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'SEND SMS VERIFICATION ERROR: {res.get("Value")}')

        return JsonResponse({
            'success': False,
            'message': 'ارسال پیامک با خطا مواجه شد. لطفا لحظاتی بعد دوباره امتحان کنید.'
        }, status=503)


class _LogoutView(LogoutView):
    template_name = 'registration/logout.html'
