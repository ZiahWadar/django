from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from rest_framework.response import Response
from . import serializer
from django.contrib.auth.models import User
from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

# Create your views here.


class PasswordReset(generics.GenericAPIView):
    serializer_class = serializer.EmailSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token =PasswordResetTokenGenerator().make_token(user)
            
            
            reset_url = reverse(
                'reset-password',
                kwargs= {'encoded_pk': encoded_pk, 'token':token}
            )
            
            reset_url = f'localhost:8000{reset_url}'
            
            return response.Response(
                {
                'message':
                    f'your password reset link: {reset_url}'
                },
                status= status.HTTP_200_OK
            )
        else:
            return response.Response(
                {
                    'message': 'User does not exist'
                },
                status=status.HTTP_400_BAD_REQUEST,
                
            )

class resetPassword(generics.GenericAPIView):
    serializer_class = serializer.ResetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data, context={'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)
        
        return Response(
            {'message': 'password reset complete'}
        )



