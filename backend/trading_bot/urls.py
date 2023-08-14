from django.urls import path
from .views import register, log_in

urlpatterns = [
    path('register/', register, name='register'),
    path('log_in/', log_in, name='log_in'),
]
