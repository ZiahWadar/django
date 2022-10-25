from django.contrib.auth.models import User

# Create your views here.

# writing the serializers inside the views but is not suppose

from rest_framework import viewsets, serializers




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
        fields = ['username', 'email', 'password', 'password2']


    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'password does not match'})
        return data
    

    # def create(self, validated_data):
    #     return User.objects.create_user(validated_data)





    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            #first_name=validated_data['first_name'],
            #last_name=validated_data['last_name'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user
