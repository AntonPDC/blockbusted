"""Accounts domain models.

We implement a custom User model because:
- you wanted email-based login
- Django's default User is username-based unless customized

Production rule: if you need a custom User model, do it from day 1.
Changing AUTH_USER_MODEL after migrations exist is painful.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    """Manager controls creation of users/superusers."""

    def create_user(self, email, password=None, username="", **extra_fields):
        # Defensive checks
        if not email:
            raise ValueError("Email is required")

        # Normalize email (lowercase domain, etc.)
        email = self.normalize_email(email)

        # Create user instance (not yet saved)
        user = self.model(email=email, username=username, **extra_fields)

        # Hash password using Django's configured password hashers
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username="admin", **extra_fields):
        # Ensure flags are correct
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, username=username, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User.

Fields:
- email: unique login identifier
- username: optional display name
- is_staff: can access Django admin
- is_active: can login or not
"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Tell Django which field is used for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
