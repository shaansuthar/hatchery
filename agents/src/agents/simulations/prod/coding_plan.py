```python
# chameleon_selling_app.py

# Import necessary libraries and modules
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.models import Token
import os

# Define the Django models for the chameleon-selling app
class Chameleon(models.Model):
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    images = models.ImageField(upload_to='chameleon_images/')

class ChameleonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chameleon
        fields = '__all__'

# Create Django REST framework viewsets for chameleons
class ChameleonViewSet(viewsets.ModelViewSet):
    queryset = Chameleon.objects.all()
    serializer_class = ChameleonSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def contact_seller(self, request, pk=None):
        # logic for contacting the seller
        return Response("Contact seller functionality under development")

    @action(detail=False, methods=['get'])
    def search_chameleons(self, request):
        # logic for searching chameleons
        return Response("Search functionality under development")

# Define the Django REST framework filters for chameleons
class ChameleonFilter(filters.FilterSet):
    class Meta:
        model = Chameleon
        fields = {
            'species': ['exact', 'contains'],
            'age': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'location': ['exact', 'contains'],
        }

# Set up Django settings for the chameleon-selling app
DEBUG = True
SECRET_KEY = 'your_secret_key'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'rest_framework']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
...
# Additional settings and configurations for the Django app
...
```

This Python code file provides a basic structure for implementing the core features of the chameleon-selling app using Django framework. It includes models for chameleons, serializers, viewsets for API endpoints, filters for search functionalities, and relevant settings and configurations. This code serves as a starting point for the development of the backend of the chameleon-selling app, aligning with the technical requirements and ensuring a reliable and scalable application.