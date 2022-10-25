from django.shortcuts import render

# Create your views here.
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
#from .utils import Util
from rest_framework import generics
from .serializers import ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response




class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    
    def post(self, request):
        data = {'request': request, 'data':request.data}

        serializer = self.serializer_class(data=request.data)
        
        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('reseting-password', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            
            print(absurl)
            email_body= 'hello \n use link below to reset your password \n ' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'reset your password'}
            #Util.send_email(data)
            
            return Response({'success': 'we have sent you a link'})
        return Response({'error': 'user not found'})

# commenting the one for checking the token

class PasswordTokenCheckAPI(generics.GenericAPIView):
    pass
#     def get(self, request, uidb64, token):
        
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
            
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'token is not valid, please request a new one' }, status=status.HTTP_401_UNAUTHORIZED)
            
#             return Response ({'success' : True, 'message': 'credentials is valid', 'uid64': uidb64, 'token': token}, status= status.HTTP_200_OK)
            
#             if not PasswordResetTokenGenerator().check_token(user):
#                 return Response({'error': 'token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
#         except DjangoUnicodeDecodeError as identifier:
#             if not PasswordResetTokenGenerator().check_token(user):
#                 return Response({'error': 'token is not valid, please request a new one' }, status=status.HTTP_401_UNAUTHORIZED)
            
            

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, tokens=kwargs)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message':'password reset successful' }, status= status.HTTP_200_OK )
