from habits.apps import HabitsConfig
from django.urls import path
from habits.views import HabitDestroyAPIView, HabitUpdateAPIView, HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('', HabitListAPIView.as_view(), name='habits_list'),
    path('view/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_view'),
    path('edit/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_edit'),
    path('delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
