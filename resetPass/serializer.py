from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ['email']
        

class ResetPasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(
        write_only = True,
        min_length = 4
    )
    class Meta:
        fields = ('password')
        
        def validate(self, data):
            print('user:', user)

            password = data.get('password')
            token = self.context.get('kwargs').get('token')
            encoded_pk = self.context('kwargd').get('encoded_pk')
            
            if token is None or encoded_pk is None:
                return serializer.validationError('missing data')
                
            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializer.validationError('the reset token is in valide')
            
            user.set_password(password)
            user.save()
            return data