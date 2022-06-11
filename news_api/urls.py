from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import NewsView


urlpatterns = [
    path('get-assessment/', NewsView.as_view(), name='get-assessment'),
    ]
