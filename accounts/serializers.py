from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=65, min_length=8, write_only=True)
  password2 = serializers.CharField(max_length=65, min_length=8, write_only=True)
  
  class Meta: 
    model = User
    fields = ['email', 'first_name', 'last_name', 'password', 'password2']
    
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    
    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords do not match'})
    return attrs
  
  def create(self, validated_data):
    email = validated_data['email']
    first_name = validated_data['first_name']
    last_name = validated_data['last_name']
    password = validated_data['password']
    
    if User.objects.filter(email=email).exists():
      raise serializers.ValidationError({'email': 'Email is already in use'})
    
    user = User.objects.create(
      email = email,
      first_name = first_name,
      last_name = last_name
    )
    user.set_password(password)
    user.save()
    return user
  
class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=6)
  password = serializers.CharField(max_length=65, write_only=True)
  full_name = serializers.CharField(max_length=255, read_only=True)
  access_token = serializers.CharField(max_length=255, read_only=True)
  refresh_token = serializers.CharField(max_length=255, read_only=True)
  
  class Meta:
    model = User
    fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']
  
  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    request = self.context.get('request')
    user = authenticate(request, email=email, password=password)
    if not user:
      raise AuthenticationFailed('Invalid credentials try again')
    user_tokens = user.tokens()
    
    