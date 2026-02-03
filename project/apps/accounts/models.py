"""Accounts models (custom User).

Why a custom User?
- Your earlier code used email as the primary login identifier.
- Django default User is username-based.
- Implementing the custom User early avoids painful migrations later.

This model is intentionally minimal:
- email (unique)
- username (optional display name)
- is_staff / is_active for admin + account control
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    """User creation helpers used by Django admin and serializers."""

    def create_user(self, email, password=None, username="", **extra_fields):
        if not email:
            raise ValueError("Email is required")

        # Normalize email to reduce duplicates like "User@X.com" vs "user@x.com"
        email = self.normalize_email(email)

        # Build user instance (not saved yet)
        user = self.model(email=email, username=username, **extra_fields)

        # Hash and store the password using Django password hashers
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username="admin", **extra_fields):
        # Ensure the flags are properly set for superusers
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, username=username, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """The actual User table."""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    # Authenticate by email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
