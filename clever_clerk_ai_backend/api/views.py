from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ( RegisterSerializer, LoginSerializer, UserSerializer, UpdateUserSerializer, ChangePasswordSerializer, CheckUsernamesSerializer )

from .models import User
from .helpers.response import api_response

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(
            api_response(
                data=UserSerializer(user).data,
                successText="User registered successfully"
            ),
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=s.validated_data["login"],
            password=s.validated_data["password"]
        )
        if not user:
            return Response({"detail":"Invalid creds"}, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = get_tokens_for_user(s.validated_data["user"])
        return Response(
            api_response(data=tokens, successText="Login successful"),
            status=status.HTTP_200_OK
        )

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):        
        return Response(
            api_response(
                data=UserSerializer(request.user).data,
                successText="User details retrieved successfully"
            ),
            status=status.HTTP_200_OK
        )
    
    def delete(self, request):
        request.user.delete()
        return Response(
            api_response(successText="User deleted"),
            status=status.HTTP_204_NO_CONTENT
        )
    
class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        ser = UpdateUserSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(
            api_response(
                data=UserSerializer(user).data,
                successText="User updated successfully"
            ),
            status=status.HTTP_200_OK
        )
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        request.user.set_password(ser.validated_data["new_password"])
        request.user.save()
        return Response(
            api_response(successText="Password reset successfully"),
            status=status.HTTP_200_OK
        )
    
class CheckUsernamesView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = CheckUsernamesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        input_list = ser.validated_data["usernames"]
        taken = set(User.objects.filter(username__in=input_list).values_list("username", flat=True))
        available = [u for u in input_list if u not in taken]
        return Response(
            api_response(
                data={"available": available},
                successText="Usernames checked successfully"
            ),
            status=status.HTTP_200_OK
        )