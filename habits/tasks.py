import os
from celery import shared_task
from loguru import logger
from datetime import timedelta

from django.utils import timezone

from habits.models import Habit
from habits.services import send_message_to_tg


@shared_task
def send_notification():  # Функция отправки уведомления
    time_now = timezone.now()
    habits = Habit.objects.filter(is_pleasant=False).all()
    token = os.getenv('TOKEN_TG_BOT')

    for habit in habits:
        if habit.owner.tg_chat_id:
            if habit.time <= time_now + timedelta(minutes=15):
                message = f"Не забудь про привычку '{habit.action}'\n" \
                          f"Запланировано выполнить в: {habit.time }"
                send_message_to_tg(token=token,
                             chat_id=habit.owner.tg_chat_id,
                             message=message)
        else:
            logger.info(f'У пользователя {habit.owner} не указан телеграм ID')

