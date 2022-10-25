from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import viewsets, serializers
from django.contrib.auth.models import User



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer