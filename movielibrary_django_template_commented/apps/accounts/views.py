"""Account views (API endpoints)."""

from rest_framework import generics, permissions
from .serializers import RegisterSerializer, MeSerializer

class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/

    Public endpoint that creates a user.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    """GET /api/accounts/me/

    Returns the currently authenticated user.
    """
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
