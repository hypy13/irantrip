from django.urls import path

from apps.account.views import LoginView, SignupView
from apps.account.views.account import UserInfoView

urlpatterns = [
    path('account/auth/login/', LoginView.as_view()),
    path('account/auth/signup/', SignupView.as_view()),

    path('account/user/', UserInfoView.as_view(), name="user-info"),

]
