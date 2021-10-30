from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import SubjectsView


urlpatterns = [
    path('subjects/', csrf_exempt(SubjectsView.as_view()), name='subjects'),
    path('subjects/<int:pk>', csrf_exempt(SubjectsView.as_view()), name='subject'),
]