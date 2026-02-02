"""DRF serializers for accounts.

Serializers:
- validate incoming JSON
- transform model objects into JSON output
"""

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    # Write-only means it is accepted in input but never returned in output
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        # Extract password so we can hash it via create_user()
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")
