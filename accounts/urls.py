from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('verify-email/', VerifyUserEamil.as_view(), name='verify-email'),
]
