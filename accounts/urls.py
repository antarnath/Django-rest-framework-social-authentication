from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('verify-email/', VerifyUserEamil.as_view(), name='verify-email'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequentView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]
