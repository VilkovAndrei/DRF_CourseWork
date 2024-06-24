from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'place', 'time')
    list_filter = ('owner',)
    search_fields = ('action',)
