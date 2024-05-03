from rest_framework import serializers
from .models import User


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