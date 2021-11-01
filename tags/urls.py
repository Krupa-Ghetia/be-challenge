from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import TagsView


urlpatterns = [
    path('tags/', csrf_exempt(TagsView.as_view()), name='lessons'),
    path('tags/<int:pk>', csrf_exempt(TagsView.as_view()), name='lesson'),
]
