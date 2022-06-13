from django.urls import path
from .views import LanguageList

urlpatterns = [
    path('v1/languages/', LanguageList.as_view()),
]
