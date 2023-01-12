from django.urls import path
from .views import health

app_name = 'account'

urlpatterns = [
    path('health/', health),
]
