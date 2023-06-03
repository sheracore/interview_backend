from rest_framework import generics
from rest_framework.permissions import AllowAny

from ..serializers import UserRegisterSerializer


class UserView(generics.CreateAPIView):
    """Create a new user in the system and return JWT token"""
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
