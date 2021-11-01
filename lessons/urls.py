from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import LessonView


urlpatterns = [
    path('lessons/', csrf_exempt(LessonView.as_view()), name='lessons'),
    path('lessons/<int:pk>', csrf_exempt(LessonView.as_view()), name='lesson'),
]
