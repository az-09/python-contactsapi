from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
from rest_framework import authentication, exceptions
# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():  # call validate in UserSerializer
            serializer.save()  # call create in UserSerializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        print('views.username', username)
        print('views.password', password)

        user = auth.authenticate(username=username, password=password)
        print('views.user', user)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY)
            print('views.auth_token', auth_token)

            serializer = UserSerializer(user)
            print('views.serializer', serializer.data)
            data = {
                'user': serializer.data,
                'token': auth_token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
