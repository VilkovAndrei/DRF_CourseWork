from habits.apps import HabitsConfig
from django.urls import path
from habits.views import HabitDestroyAPIView, HabitUpdateAPIView, HabitListAPIView, HabitCreateAPIView, \
    HabitRetrieveAPIView, PublicHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habits/list/', HabitListAPIView.as_view(), name='habits_list'),
    path('habits/public_list/', PublicHabitListAPIView.as_view(), name='habits_public_list'),
    path('habits/view/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_view'),
    path('habits/edit/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_edit'),
    path('habits/delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
