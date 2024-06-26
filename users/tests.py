from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):

    def test_register(self):

        self.client.post('/users/register/', {
            'email': 'user55@test.com',
            'password': '1234Qwerty5678',
            'password2': '1234',
            'tg_chat_id': 3455539408
        })

        self.assertRaises(ValidationError, msg={
            "password": "Password fields didn't match."
        })

        response = self.client.post('/users/register/', {
            'email': 'user55@test.com',
            'password': '1234Qwerty5678',
            'password2': '1234Qwerty5678',
            'tg_chat_id': 3455539408
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(User.objects.filter(email='user55@test.com').exists())
