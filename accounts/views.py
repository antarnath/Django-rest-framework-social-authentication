from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword

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