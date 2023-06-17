from django.urls import path
from service.views import get_service

urlpatterns = [
    path('vanya-service',get_service,name = "service")
]