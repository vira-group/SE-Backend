import json
from rest_framework import status
from django.test import TestCase
from . import models
import json
from urllib import response
import http
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import User
from .serializers import user_serializers


class UserRegisterAPITests(TestCase):
    def setUp(self):
        self.url = "/api/auth/users/"
        return super().setUp()

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_register(self):
        '''
        testing normal register process
        '''
        data = {"email": "hediyeh.eshaqi@gmail.com", "password": "strongpass", "re_password": "strongpass"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_wrong_pasword(self):
        '''
        sending request with no password
        '''
        data = {"email": "eshaqi.ce@gmail.com", "password": "", "re_password": "strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_wrong_email(self):
        '''
        sending request with email by incorrect format
        '''
        data = {"email": "eshaqi.cemailcom", "password": "strongpass", "re_password": "strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_email(self):
        '''
        sending request with no email
        '''
        data = {"email": "", "password": "strongpass", "re_password": "strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_bad_password(self):
        '''
        full numeric password
        '''
        data = {"email": "eshaqi.cemailcom", "password": "1", "re_password": "1"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_repassword_nomatch(self):
        data = {"email": "eshaqi.cemailcom", "password": "1", "re_password": "2"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginApiTest(APITestCase):
    def setUp(self) -> None:
        data = {"email": "hello@gmail.com", "password": "strongpass", "re_password": "strongpass"}
        self.client.post("/api/auth/users/", data)
        user = get_user_model().objects.get(email="hello@gmail.com")
        user.is_active = True
        user.save()
        data1 = {"email": "hello1@gmail.com", "password": "strongpass1", "re_password": "strongpass1"}
        self.client.post("/api/auth/users/", data)
        user = get_user_model().objects.get(email="hello@gmail.com")
        user.save()

    def test_login_normal(self):
        data = {"email": "hello@gmail.com", "password": "strongpass"}
        response = self.client.post("/api/auth/token/login/", data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_without_emailVerification(self):
        data = {"email": "hello1@gmail.com", "password": "strongpass1"}
        response = self.client.post("/api/auth/token/login/", data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        data = {"email": "hello1@gmail.com", "password": "str"}
        response = self.client.post("/api/auth/token/login/", data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPaymentAPITest(APITestCase):

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create(is_active=True, email="nima.kam@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(is_active=True, email="mohammad@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.user3 = get_user_model().objects.create(is_active=True, email="reza@gmail.com")
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

    def test_pay_unauth(self):
        data = {"credit": 10}
        resp = self.client.post(reverse.reverse("add_credit-list"), data=data)
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_pay_not_valid(self):
        self.set_credential(self.token1)
        data = {"credit": -10}
        resp = self.client.post(reverse.reverse("add_credit-list"), data=data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"credit": 'NaN'}
        resp = self.client.post(reverse.reverse("add_credit-list"), data=data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_pay_success(self):
        self.set_credential(self.token1)
        data = {"credit": 10}
        old_cred = get_user_model().objects.get(pk=1).balance
        resp = self.client.post(reverse.reverse("add_credit-list"), data=data)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        new_cred = get_user_model().objects.get(pk=1).balance
        self.assertEqual(old_cred + data['credit'], new_cred)
