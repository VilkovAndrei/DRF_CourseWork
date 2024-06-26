from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from habits.serializers import HabitSerializer
from habits.models import Habit
from habits.paginations import HabitPaginator

from users.permissions import IsOwner, IsSuperuser


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAdminUser | IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            queryset = Habit.objects.filter(owner=user).order_by('id')
        else:
            queryset = Habit.objects.all().order_by('id')
        return queryset


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        queryset = Habit.objects.filter(is_public=True).order_by('id')

        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner | IsSuperuser, )


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner | IsSuperuser, )


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsOwner | IsSuperuser, )
