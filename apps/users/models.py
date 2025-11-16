from __future__ import annotations
from typing import Optional
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.conf import settings


DEPARTMENT_CHOICES = [
    ("IT", "IT"),
    ("HR", "HR"),
    ("Sales", "Sales"),
    ("Finance", "Finance"),
]

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("manager", "Manager"),
    ("employee", "Employee"),
]


class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, username: str, password: Optional[str] = None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, username: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    Required fields:
      - email (unique)
      - username
      - first_name
      - last_name
      - phone
      - city
      - country
      - department
      - role
      - birth_date (nullable)
      - salary
      - is_active, is_staff, date_joined, last_login (standard)
    """
    email: str = models.EmailField(unique=True)
    username: str = models.CharField(max_length=150, unique=True)
    first_name: str = models.CharField(max_length=150)
    last_name: str = models.CharField(max_length=150)
    phone: str = models.CharField(max_length=30, blank=True)
    city: str = models.CharField(max_length=100, blank=True)
    country: str = models.CharField(max_length=100, blank=True)
    department: str = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    role: str = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    birth_date: Optional[models.DateField] = models.DateField(null=True, blank=True)
    salary: Optional[models.DecimalField] = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    # standard fields
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)
    date_joined: timezone.datetime = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.email}"
