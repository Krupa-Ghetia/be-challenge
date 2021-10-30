from django.urls import path

from .views import UserRegistrationView


urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_registration')
]