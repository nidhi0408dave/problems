from django.urls import path
from .views import APIViewWithDDOSProtection

urlpatterns = [
    path('', APIViewWithDDOSProtection.as_view(), name='api_view')
]
