import json
from rest_framework import status
from django.test import TestCase
from main import models
import json
from urllib import response
import http
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from main.models import User
from main.serializers import user_serializers

class UserRegisterAPITests(TestCase):
    def setUp(self):
        self.url = ("/auth/users/")
        return super().setUp()

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_register(self):
        '''
        testing normal register process
        '''
        data = {"email":"hediyeh.eshaqi@gmail.com","password":"strongpass","re_password":"strongpass"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_wrong_pasword(self):
        '''
        sending request with no password
        '''
        data = {"email":"eshaqi.ce@gmail.com","password":"","re_password":"strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_wrong_email(self):
        '''
        sending request with email by incorrect format
        '''
        data = {"email":"eshaqi.cemailcom","password":"strongpass","re_password":"strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_email(self):
        '''
        sending request with no email
        '''
        data = {"email":"","password":"strongpass","re_password":"strongpass"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_bad_password(self):
        '''
        full numeric password
        '''
        data = {"email":"eshaqi.cemailcom","password":"1","re_password":"1"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_repassword_nomatch(self):
        data = {"email":"eshaqi.cemailcom","password":"1","re_password":"2"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


