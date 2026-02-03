"""Account API endpoints."""

from rest_framework import generics, permissions
from .serializers import RegisterSerializer, MeSerializer

class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/

    Public endpoint to create an account.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    """GET /api/accounts/me/

    Authenticated endpoint that returns the currently logged-in user.
    """
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
