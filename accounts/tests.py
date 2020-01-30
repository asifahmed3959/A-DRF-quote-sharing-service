from unittest import mock

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AccountRegistrationTest(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('accounts:registration')
        data = {
            'username':"targerian",
            "first_name":"Aegon",
            "last_name":"Targerian",
            "email":"jon_snow@gmail.com",
            "password":"-->1john1<--"
        }
        response = self.client.post(url,data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del data["password"]
        self.assertEqual(response.data,data)


class PasswordChangeTest(APITestCase):

    login_url = reverse('accounts:login')
    refresh_token_url = reverse('accounts:token_refresh')
    logout_url = reverse('accounts:logout')

    email = "jon_snow@gmail.com"
    password = "-->1john1<--"
    first_name = "jon"
    last_name = "snow"
    username = "jon_snow"

    def setUp(self):
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        data = {
            'username': self.username,
            'password': self.password
        }
        r = self.client.post(self.login_url, data)
        body = r.json()
        if 'access' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access'])


    def test_change_password(self):

        url = reverse('accounts:change_password')
        data = {
            "old_password": "-->1john1<--",
            "new_password": "1-->john<--1"
        }

        response = self.client.put(url, data, format='json')
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password(data['new_password']))