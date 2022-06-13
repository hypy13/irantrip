from apps.account.models import User
from apps.account.views.auth import generate_login_token


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        #
        # user = User.objects.first()
        # request.META['HTTP_AUTHORIZATION'] = "Token " + generate_login_token(user)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
