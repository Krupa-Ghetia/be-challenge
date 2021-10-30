from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.views.decorators.csrf import csrf_exempt



from .views import UserRegistrationView, UserView


urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', csrf_exempt(UserView.as_view()), name='user'),
]