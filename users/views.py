from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.permissions import IsSuperuser, IsOwner
from users.serializers import UserRegisterSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [IsSuperuser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsSuperuser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
