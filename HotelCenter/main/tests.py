import http
from django.test import TestCase
import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Hotel


class UserTestCase(APITestCase):
    test_urls = {
        "hotel-list": "/hotel/hotels/",
        "hotel-obj": "/hotel/hotels/{}/",
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """
        self.user1_data = {
            "email": "",
            'password': "",
            "repassword": "",
        }

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


    def test_register_success(self):
        pass

    def test_register_fields_miss(self):
        pass

    def test_login_success(self):
        pass

    def test_login_fail(self):
        pass

    def test_activation(self):
        pass
