from django.urls import path, include
from resetPass import views

urlpatterns = [
    path('password-resett/<str:encoded_pk>/<str:token>/', views.resetPassword.as_view(), name='reset-password'),
    path('password-resett/', views.PasswordReset.as_view(), name='reset-password'),
]
