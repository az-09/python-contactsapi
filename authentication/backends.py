import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        print('backends.auth_data', auth_data.decode('utf-8').split(' '))

        if not auth_data:
            print('backends.auth_data None triggered')
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms="HS256")
            print('backends.payload', payload)
            user = User.objects.get(username=payload['username'])

            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired')
        return super().authenticate(request)
