from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, **extra):
        if not email or not username or not name or not password:
            raise ValueError("Required fields are missing")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name     = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email    = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # hashed via set_password()
    image    = models.BinaryField(null=True, blank=True)
    is_active= models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "password"]
