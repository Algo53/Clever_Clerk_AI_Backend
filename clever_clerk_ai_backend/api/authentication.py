from rest_framework import exceptions
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication

from .models import User

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None

class CustomJWTAuthentication(BaseJWTAuthentication):
    def authenticate(self, request):
            """
            Attempt to read and validate the Access Token from the Authorization header.
            Returns a `(user, token)` tuple or raises AuthenticationFailed.
            """
            header = self.get_header(request)
            if header is None:
                return None

             # Decode + split
            header_str = header.decode("utf-8")
            try:
                scheme, token_str = header_str.split()
            except ValueError:
                raise exceptions.AuthenticationFailed("Invalid Authorization header format.")

            if token_str is None:
                raise exceptions.AuthenticationFailed('Invalid token header.')

            # Validate signature and expiry
            try:
                validated_token = self.get_validated_token(token_str)
            except Exception as e:
                print("‼️ token validation error:", e)
                raise

            # Fetch user
            try:
                user = self.get_user(validated_token)
            except Exception as e:
                print("‼️ get_user error:", e)
                raise exceptions.AuthenticationFailed("Could not fetch user from token.")

            if not getattr(user, 'is_active', False):
                raise exceptions.AuthenticationFailed('User account is disabled.')

            return (user, validated_token)