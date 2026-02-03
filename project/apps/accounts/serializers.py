"""DRF serializers for accounts.

Serializers handle:
- input validation
- output shaping

We keep Register separate from Me to control what fields are exposed.
"""

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    # write_only prevents returning password back to client
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        # Use the model manager to ensure password hashing is correct
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")
