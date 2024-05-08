from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.exceptions import TokenError


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
    if not user.is_verified:
      raise AuthenticationFailed('Account is not verified')
    user_tokens = user.tokens()
    
    return {
      'email': user.email,
      'full_name': user.get_full_name,
      'access_token': str(user_tokens['access']),
      'refresh_token': str(user_tokens['refresh'])
    }

class PasswordResetRequestSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255, min_length=6)
  
  class Meta:
    model = User
    fields = ['email']
    
  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      request = self.context.get('request')
      site_domain = get_current_site(request).domain
      relative_link = reverse(
        'password-reset-confirm',
        kwargs={'uidb64': uidb64, 'token': token}
      )
      print('================================================================')
      print("site_domain", site_domain)
      print("relative_link", relative_link)
      frontend_domain = 'http://localhost:5173'
      abslink = f'http://{site_domain}{relative_link}'
      email_body = f'Hi use the link below to reset your password \n {abslink}'
      data = {
        'email_body': email_body,
        'email_subject': 'Reset your password',
        'to_email': user.email
      }
      send_normal_email(data)
    return super().validate(attrs)
  
class SetNewPasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=65, write_only=True)
  confirm_password = serializers.CharField(max_length=65, write_only=True) 
  uidb64 = serializers.CharField(write_only=True)
  token = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = ['uidb64', 'token', 'password', 'confirm_password']
    
  def validate(self, attrs):
    try:
      token = attrs.get('token')
      uidb64 = attrs.get('uidb64')
      password = attrs.get('password')
      confirm_password = attrs.get('confirm_password')
      print("========Set New Password Serializer========")
      print("token", token)
      user_id = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=user_id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise AuthenticationFailed('The reset link is invalid', 401)
      if password != confirm_password:
        raise AuthenticationFailed('Passwords do not match')
      user.set_password(password)
      user.save()
      return user
    except Exception as e:
      return AuthenticationFailed('The reset link is invalid', 401)
    
class LogoutUserSerializer(serializers.Serializer):
  refresh_token = serializers.CharField()
  
  default_error_message = {
    'bad_token': ('Token is invalid or expired'),
  }
  
  def validate(self, attrs):
    self.token = attrs['refresh_token']
    return attrs
  
  def save(self, **kwargs):
    try:
      token = RefreshToken(self.token)
      token.blacklist()
    except TokenError:
      self.fail('bad_token') 
  