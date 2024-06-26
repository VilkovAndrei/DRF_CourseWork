from django.utils import timezone

from django.core.management import BaseCommand

from habits.models import Habit
from loguru import logger


logger.add("patch_habits_time.log", format="{time} {level} {message}", level="INFO", rotation="1 week")


class Command(BaseCommand):

    def handle(self, *args, **options):
        count_patchs = 0  # счетчик исправлений
        time_now = timezone.now()
        habits = Habit.objects.all()
        for habit in habits:
            if habit.time <= time_now:
                time_for_patch = habit.time
                while time_for_patch <= time_now:
                    time_for_patch += habit.frequency
                habit.time = time_for_patch
                habit.save()
                count_patchs += 1
                logger.info(f'Исправлено время привычки {str(habit)} на:{habit.time}')

        if count_patchs == 0:
            logger.info(f'В базе нет неправильных (в прошлом) времен привычек.')
        else:
            logger.info(f'В базе исправлено {count_patchs} времен привычек.')
