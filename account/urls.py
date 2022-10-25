#from .views import RegisterAPI
from django.urls import path, include
from knox import views as knox_views
from .views import LoginAPI
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView

router = DefaultRouter()
router.register('anotherReg', UserViewSet, basename='anotherReg')


urlpatterns = [
    path('', include(router.urls)),
    #path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('request_reset_email/', RequestPasswordResetEmail.as_view(), name='request_reset_email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    
    path('password-reset-chech/', PasswordTokenCheckAPI.as_view(), name='password-reset-check'),
]



