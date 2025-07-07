from rest_framework import serializers
from .helpers.fields import Base64ImageField
from django.contrib.auth import authenticate

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model  = User
        fields = ["name", "username", "email", "password", "image"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated):
        password = validated.pop("password")
        user = User.objects.create_user(password=password, **validated)
        return user

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["login"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data
        
class UserSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "image"]

class UpdateUserSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ["name", "username", "email", "image"]
        extra_kwargs = {"email": {"required": False}}

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Invalid old password")
        return value
    
class CheckUsernamesSerializer(serializers.Serializer):
    username = serializers.ListField(
        child=serializers.CharField(max_length=10, min_length=4), write_only= True
    )