from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
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
    