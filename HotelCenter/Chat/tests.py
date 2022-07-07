from django.test import TestCase

from rest_framework import status, reverse
from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase



class chatTestCase(APITestCase):
    test_urls = {
        "user-chatlist": '/api/chat/mychatlist/',
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """

        self.user1 = get_user_model().objects.create(is_active=True, email="hediyeh@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(is_active=True, email="hediyeh1@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.user3 = get_user_model().objects.create(is_active=True, email="hediyeh3@gmail.com")
        self.user3.set_password("some-strong2pass")
        self.user3.save()

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.user3)

    def set_credential(self, token):
        """
            set token for authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def unset_credential(self):
        """
            unset existing headers
        """
        self.client.credentials()

    def test_user_chatlist_success(self):
        self.set_credential(token=self.token1)
        response = self.client.get(self.test_urls["user-chatlist"])
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_chatlist_unauthorized(self):
        self.unset_credential()
        response = self.client.get(self.test_urls["user-chatlist"])
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)