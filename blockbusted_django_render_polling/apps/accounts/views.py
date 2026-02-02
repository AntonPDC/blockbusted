from rest_framework import generics, permissions
from .serializers import RegisterSerializer, MeSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer
    def get_object(self):
        return self.request.user
