from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import CourseView


urlpatterns = [
    path('courses/', csrf_exempt(CourseView.as_view()), name='subject_courses'),
]
