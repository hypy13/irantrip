from apps.clientside.views.registration import LoginForm, RegistrationForm


def registration_form(request):
    return {
        'login': LoginForm(),
        'register': RegistrationForm()
    }
