


from rest_framework.response import Response
from rest_framework import status

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




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
        
    def validate(self, attrs, **kwargs):
        print(kwargs)
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
         