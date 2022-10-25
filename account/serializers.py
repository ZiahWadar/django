from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# from .utils import Util
from rest_framework.response import Response
from rest_framework import status



MIN_LENGTH = 6

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length": f"password most be longer than {MIN_LENGTH} character."
        }
        
    )
    
    password2 = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length": f"password most be longer than {MIN_LENGTH} character",
        }
        
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']


    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'password does not match'})
        return Response({'success': 'we have sent you an email to reset your password'}, status=status.HTTP_200_OK)
    
    
    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email = validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
    )
    
        user.set_password(validated_data['password'])
        user.save()
        
        return user
# reset password

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    
    class Meta:
        fields = ['email']
    
    

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True, max_length=68)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password']
        
    def validate(self, attrs):

        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('the reset link has expire', 401)
        user.set_password(password)
        user.save()
        return (user)
        
        # else:
        #     print('hello')
        #     raise serializers.ValidationError('the reset link is invalid invalid', 401)
        return super().validate(attrs)
            



    
# change password
    
# from rest_framework import serializers
# from django.contrib.auth.models import User

# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')

# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

#         return user