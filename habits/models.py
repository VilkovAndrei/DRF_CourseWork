from datetime import timedelta

from django.db import models

from users.models import User, NULLABLE

HABIT_MODEL = 'habits.Habit'


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    place = models.CharField(max_length=100, verbose_name='место действия')
    time = models.DateTimeField(verbose_name='время')
    action = models.CharField(max_length=150, verbose_name='действие')
    frequency = models.DurationField(default=timedelta(days=1), verbose_name='периодичность')
    time_to_complete = models.DurationField(default=timedelta(minutes=1), verbose_name='продолжительность действия')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')

    connected_habit = models.ForeignKey(HABIT_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                        verbose_name='связанная привычка')
    reward = models.CharField(max_length=200, **NULLABLE, verbose_name='награда')

    def __str__(self):
        return f"{self.action} in {self.place} at {self.time}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
