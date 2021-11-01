from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import VideoView


urlpatterns = [
    path('videos/', csrf_exempt(VideoView.as_view()), name='lessons'),
    path('videos/<int:pk>', csrf_exempt(VideoView.as_view()), name='lesson'),
]
