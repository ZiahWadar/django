from .views import ChangePasswordView
from django.urls import path, include

urlpatterns = [
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]