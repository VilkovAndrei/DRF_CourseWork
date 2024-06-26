from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def test_register(self):
        pass

        # response = self.client.post('/users/register/', {
        #     'email': 'user55@test.com',
        #     'password': '1234Qwerty',
        #     'password2': '1234Qwerty',
        #     'tg_chat_id': 3455539408
        # })
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(User.objects.filter(email='user55@test.com').exists())
