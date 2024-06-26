from rest_framework import serializers

from habits.models import Habit
from habits.validators import BigRewardValidator, ExecTimeValidator, ConnectedHabitValidator, \
    PleasantHabitValidator, FrequencyValidator, TimeValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            BigRewardValidator(),
            ExecTimeValidator(),
            ConnectedHabitValidator(),
            PleasantHabitValidator(),
            FrequencyValidator(),
            TimeValidator()
        ]

    def create(self, validated_data):
        new_habit = Habit.objects.create(**validated_data)
        new_habit.owner = self.context.get('request').user
        new_habit.save()

        return new_habit
