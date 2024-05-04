from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import (
  UserRegisterSerializer, 
  LoginSerializer, 
  PasswordResetRequestSerializer,
  SetNewPasswordSerializer,
  LogoutUserSerializer
)
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegisterUser(GenericAPIView):
  serializer_class = UserRegisterSerializer
  
  def post(self, request):
    user_data = request.data
    serializer = self.serializer_class(data=user_data)
    if serializer.is_valid():
      serializer.save()
      user = serializer.data
      # send email function user['email']
      send_code_to_user(user['email'])
      return Response({
        'data': user,
        'message': f'hi {user['first_name']} thanks for registering. Please verify your email. You received a passcord in your email.'
      }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class VerifyUserEamil(GenericAPIView):
  def post(self, request):
    otp_code = request.data.get('otp')
    try:
      user_code_obj = OneTimePassword.objects.get(code=otp_code)
      user = user_code_obj.user
      if not user.is_verified:
        user.is_verified = True
        user.save()
        return Response({
          'message': 'account verified successfully'
        }, status=status.HTTP_200_OK)
      else:
        return Response({
          'message': 'account already verified'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except OneTimePassword.DoesNotExist:
      return Response({
        'message': 'invalid passcode'
      }, status=status.HTTP_404_NOT_FOUND)
      
class LoginUser(GenericAPIView):
  serializer_class = LoginSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class TestAuthenticationView(GenericAPIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    return Response({'message': 'You are authenticated'}, status=status.HTTP_200_OK)
  
class PasswordResetRequentView(GenericAPIView):
  serializer_class = PasswordResetRequestSerializer
  # permission_classes = [IsAuthenticated]
  def post(self, request):
    serializer = self.serializer_class(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(
      {'message': 'Password reset email has been sent'},
      status=status.HTTP_200_OK
    )
    
    
class PasswordResetConfirmView(GenericAPIView):
  def get(self, request, uidb64, token):
    try:
      user_id = smart_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=user_id) 
      if not PasswordResetTokenGenerator().check_token(user, token):
        return Response(
          {'message': 'Token is invalid or expired. Please request a new one'},
          status=status.HTTP_401_UNAUTHORIZED
        )
      return Response(
        {'success': True,'message': 'Credentials valid, can reset password', 'uidb64': uidb64, 'token': token},
        status=status.HTTP_200_OK
      )
    except DjangoUnicodeDecodeError as identifier:
      return Response(
        {'message': 'Token is invalid or expired. Please request a new one'},
        status=status.HTTP_401_UNAUTHORIZED
      )
      
class SetNewPasswordView(GenericAPIView):
  serializer_class = SetNewPasswordSerializer
  def patch(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(
      {'message': 'Password reset success'},
      status=status.HTTP_200_OK
   )
    
class LogoutUserView(GenericAPIView):
  serializer_class = LogoutUserSerializer
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    serializer = self.serializer_class(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    print(request.data)
    return Response(
      {'message': 'Logout success'},
      status=status.HTTP_204_NO_CONTENT
    )