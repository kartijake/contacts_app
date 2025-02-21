from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """Manager for custom User model with email authentication"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email for authentication"""
    
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email
