from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserUpdateSerializer

    def get_object(self):
        return self.request.user
