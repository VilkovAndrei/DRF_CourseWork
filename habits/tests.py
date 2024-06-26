from datetime import datetime, timezone, timedelta

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.validators import ValidationError

from habits.models import Habit
from habits.tasks import send_notification
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            email='user@test.com',
            tg_chat_id=5332103807
        )
        self.test_user.set_password('1234')
        self.test_user.save()

        self.client.force_authenticate(user=self.test_user)

        self.test_habit = Habit.objects.create(
            owner=self.test_user,
            place='тестовое место',
            time=datetime.now(timezone.utc) + timedelta(minutes=10),
            action='тестовое действие',
            time_to_complete=timedelta(minutes=1),
            is_public=True,
            is_pleasant=False,
            frequency=timedelta(days=1)
        )

        self.test_pleasant_habit = Habit.objects.create(
            owner=self.test_user,
            place='test nasty place',
            time=datetime.now(timezone.utc) + timedelta(days=1),
            action='test reward action',
            time_to_complete=timedelta(minutes=1),
            is_pleasant=True
        )

    def test_list(self):
        """ Тестирование списка привычек """
        response = self.client.get('/habits/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_public_list(self):
        """ Тестирование списка публичных привычек """
        response = self.client.get('/habits/public_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

    def test_retrieve(self):
        """ Тестирование просмотра привычки """
        response = self.client.get(f'/habits/view/{self.test_habit.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['place'], 'тестовое место')

    def test_create(self):
        """ Тестирование создания привычки """
        response = self.client.post('/habits/create/', {
            'place': 'другое место',
            'time': datetime.now(timezone.utc) + timedelta(hours=1),
            'action': 'другое действие',
            'time_to_complete': timedelta(minutes=1),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(place='другое место').exists())

    def test_update(self):
        """ Тестирование редактирования привычки """
        response = self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'time': self.test_habit.time,
            'action': self.test_habit.action,
            'time_to_complete': self.test_habit.time_to_complete,

            'reward': 'награда ждет'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(pk=self.test_habit.pk).reward, 'награда ждет')

    def test_destroy(self):
        """ Тестирование удаления привычки """
        bad_user = User.objects.create(email='bad_user@test.com',
                                       tg_chat_id=3475552909,
                                       password='1234')
        self.client.force_authenticate(user=bad_user)

        path = reverse('habits:habit_delete', [self.test_habit.pk])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not Habit.objects.filter(pk=self.test_habit.pk).exists())

    def test_bigreward_validator(self):
        """ Тестирование валидатора привычки BigRewardValidator"""
        self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'time': self.test_habit.time,
            'action': self.test_habit.action,
            'time_to_complete': self.test_habit.time_to_complete,

            'reward': 'награда ждет',
            'connected_habit': self.test_pleasant_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "big_reward": "Нельзя заполнять одновременно и поле вознаграждения, и поле связанной привычки."
        })

    def test_time_to_complete_validator(self):
        """ Тестирование валидатора привычки ExecTimeValidator"""
        self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'time': self.test_habit.time,
            'action': self.test_habit.action,

            'time_to_complete': timedelta(minutes=10)
        })
        self.assertRaises(ValidationError, msg={
            "time_to_complete": "Время выполнения должно быть не больше 2 минут."
        })

    def test_connected_habit_validator(self):
        """ Тестирование валидатора привычки ConnectedHabitValidator"""
        self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'time': self.test_habit.time,
            'action': self.test_habit.action,
            'time_to_complete': self.test_habit.time_to_complete,

            'connected_habit': self.test_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "connected_habit": "В связанные привычки могут попадать"
                               " только привычки с признаком приятной привычки."
        })

    def test_pleasant_habit_validator(self):
        """ Тестирование валидатора привычки PleasantHabitValidator"""
        self.client.put(f'/habits/edit/{self.test_pleasant_habit.pk}/', {
            'place': self.test_pleasant_habit.place,
            'time': self.test_pleasant_habit.time,
            'action': self.test_pleasant_habit.action,
            'time_to_complete': self.test_pleasant_habit.time_to_complete,

            'connected_habit': self.test_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "is_pleasant": "У приятной привычки не может быть вознаграждения или связанной привычки."
        })

        self.client.put(f'/habits/{self.test_pleasant_habit.pk}/', {
            'place': self.test_pleasant_habit.place,
            'time': self.test_pleasant_habit.time,
            'action': self.test_pleasant_habit.action,
            'time_to_complete': self.test_pleasant_habit.time_to_complete,

            'reward': 'награда ждет'
        })
        self.assertRaises(ValidationError, msg={
            "is_pleasant": "У приятной привычки не может быть вознаграждения или связанной привычки."
        })

    def test_frequency_validator(self):
        """ Тестирование валидатора привычки FrequencyValidator"""
        self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'time': self.test_habit.time,
            'action': self.test_habit.action,
            'time_to_complete': self.test_habit.time_to_complete,

            'frequency': timedelta(days=8)
        })
        self.assertRaises(ValidationError, msg={
            "frequency": "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
        })

    def test_time_validator(self):
        """ Тестирование валидатора привычки TimeValidator"""
        self.client.put(f'/habits/edit/{self.test_habit.pk}/', {
            'place': self.test_habit.place,
            'action': self.test_habit.action,
            'time_to_complete': self.test_habit.time_to_complete,

            'time': datetime.now(timezone.utc) - timedelta(days=1)
        })
        self.assertRaises(ValidationError, msg={
            'time': 'Время старта привычки не может быть меньше текущего времени + 5 минут.'
        })

    def test_tasks(self):
        """ Тестирование отправки сообщения в телеграм"""
        test_time = self.test_habit.time + self.test_habit.frequency
        send_notification()
        self.assertEqual(Habit.objects.get(pk=self.test_habit.pk).time, test_time)
