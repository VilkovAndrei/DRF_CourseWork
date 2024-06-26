from rest_framework import generics, status

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsSuperuser, IsOwner
from users.serializers import UserRegisterSerializer, UserSerializer, MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsOwner | IsSuperuser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsOwner | IsSuperuser]
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
