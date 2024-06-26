import os
from celery import shared_task
from loguru import logger
from datetime import timedelta

from django.utils import timezone

from config.settings import TIMEDELTA_NOTIFICATION
from habits.models import Habit
from habits.services import send_message_to_tg


logger.add("habits.log", format="{time} {level} {message}", level="INFO", rotation="1 week")


@shared_task
def send_notification():  # Функция отправки уведомления
    time_now = timezone.now()
    habits = Habit.objects.filter(is_pleasant=False).all()
    token = os.getenv('TOKEN_TG_BOT')

    for habit in habits:
        user_tg_chat_id = habit.owner.tg_chat_id
        connected_habit_action = ''
        habit_reward = habit.reward
        if habit.connected_habit:
            habit_reward = ""
            connected_habit_action = habit.connected_habit.action
        if user_tg_chat_id:
            if habit.time <= time_now + timedelta(minutes=TIMEDELTA_NOTIFICATION):
                message = f"Не забудь про привычку '{habit.action}'\n" \
                          f"Запланировано выполнить в: {habit.time}\n" \
                          f"После выполнения приятная привычка '{connected_habit_action}'\n" \
                          f"или вознаграждение: '{habit_reward}'"
                send_message_to_tg(token=token,
                                   chat_id=user_tg_chat_id,
                                   message=message)
                habit.time += habit.frequency
                habit.save()
                logger.info(f'Пользователю {habit.owner} отправлено напоминание в телеграм id:{user_tg_chat_id}')
        else:
            logger.info(f'У пользователя {habit.owner} не указан телеграм ID')
