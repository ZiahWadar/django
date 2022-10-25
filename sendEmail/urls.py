from .views import PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView
from django.urls import path, include
    
    
urlpatterns = [
    path('request-email/', RequestPasswordResetEmail.as_view(), name='request-email'),
    #path('password-request/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-request'),
    path('reseting-password/<uidb64>/<token>/', SetNewPasswordAPIView.as_view(), name='reseting-password'),
    ]
    