from datetime import timedelta

from django.db import models

from users.models import User, NULLABLE

HABIT_MODEL = 'habits.Habit'


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    place = models.CharField(max_length=100)
    time = models.DateTimeField()
    action = models.CharField(max_length=150)
    frequency = models.DurationField(default=timedelta(days=1))
    time_to_complete = models.DurationField()
    is_public = models.BooleanField(default=False)
    is_pleasant = models.BooleanField(default=False)

    connected_habit = models.ForeignKey(HABIT_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    reward = models.CharField(max_length=200, **NULLABLE)

    def __str__(self):
        return f"{self.action} in {self.place} at {self.time}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
