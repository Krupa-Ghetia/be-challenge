from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import CourseView


urlpatterns = [
    path('courses/', csrf_exempt(CourseView.as_view()), name='courses'),
    path('courses/<int:pk>', csrf_exempt(CourseView.as_view()), name='course'),
    path('courses/<int:course>/', include('lessons.course_lessons_urls')),
]
