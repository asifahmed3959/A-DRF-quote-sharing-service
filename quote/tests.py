from django.test import TestCase

from unittest import mock

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import QuoteListSerializer

from functools import partial

from .models import Quote

import json


User = get_user_model()


class CreateQuoteTest(APITestCase):

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
            username = self.username,
            email = self.email,
            password = self.password,
            first_name = self.first_name,
            last_name = self.last_name
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


    def test_create_quote(self):
        """
        Ensure we can create a new quote object.
        """
        url = reverse('quote:create_view', kwargs={'pk':self.user.id})
        data = {
            "quote": "J aime pelle Jon Snow, and I believe whitewalkers should die",
            "author": self.user.id
                    }
        response = self.client.post(url,data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,data)


    def test_get_quote(self):
        """
        Ensure quote can be retrieved via id,username or any text in the quote
        """
        url = reverse('quote:quote_view')
        quote_size = Quote.objects.all().count()

        response = self.client.get(url,format = 'json')

        self.assertEqual(len(response.data),quote_size)

        quote = Quote(author = self.user, quote = "May this world end")
        quote.save()

        data = {
         "text": "world"
        }
        response = self.client.get(url, data, format='json')
        dict = (response.data[0])
        self.assertEqual(dict["quote"], quote.quote)

        data = {
            "id" : quote.id
        }

        response = self.client.get(url,data,format = 'json')
        dict = (response.data[0])
        self.assertEqual(dict['id'],quote.id)

        data = {
            "username":self.username
        }

        response = self.client.get(url,data,format = 'json')
        dict = (response.data[0])
        self.assertEqual(dict['author']['username'] , self.user.username)


    def test_retrieve_update_delete(self):
        """
        Ensuring that quote can be retrieved, updated and deleted
        by a user.
        """

        quote = Quote(author=self.user, quote="May this world end")
        quote.save()

        url = reverse('quote:quote_detail_view', kwargs={'pk': quote.id})
        data = {
            "quote": "May this world end",
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, data)

        data = {
            "quote": "May this world never end",
        }

        response = self.client.put(url,data, format='json')
        self.assertEqual(response.data,data)

        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)