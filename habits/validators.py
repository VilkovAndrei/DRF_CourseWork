from datetime import datetime, timedelta, timezone

from rest_framework.validators import ValidationError


class BigRewardValidator:
    def __call__(self, attrs):
        if {'connected_habit', 'reward'}.issubset(attrs.keys()):
            if attrs['reward'] and attrs['connected_habit']:
                raise ValidationError({
                    "big_reward": "Нельзя заполнять одновременно и поле вознаграждения, и поле связанной привычки."
                })


class ExecTimeValidator:
    def __call__(self, attrs):
        if attrs['time_to_complete'] > timedelta(minutes=2):
            raise ValidationError({
                "time_to_complete": "Время выполнения должно быть не больше 2 минут."
            })


class ConnectedHabitValidator:
    def __call__(self, attrs):
        if {'connected_habit'}.issubset(attrs.keys()):
            if attrs['connected_habit'] and not attrs['connected_habit'].is_pleasant:
                raise ValidationError({
                    "connected_habit": "В связанные привычки могут попадать"
                                       " только привычки с признаком приятной привычки."
                })


class PleasantHabitValidator:
    def __call__(self, attrs):
        if {'connected_habit', 'is_pleasant', 'reward'}.issubset(attrs.keys()):
            if attrs['is_pleasant'] and (attrs['connected_habit'] or attrs['reward']):
                raise ValidationError({
                    "is_pleasant": "У приятной привычки не может быть вознаграждения или связанной привычки."
                })


class FrequencyValidator:
    def __call__(self, attrs):
        if 'frequency' in attrs.keys() and attrs['frequency'] > timedelta(days=7):
            raise ValidationError({
                "frequency": "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            })


class TimeValidator:
    def __call__(self, attrs):
        if attrs['time'] < datetime.now(timezone.utc) + timedelta(minutes=5):
            raise ValidationError({
                'time': 'Время старта привычки не может быть меньше текущего времени + 5 минут.'
            })
