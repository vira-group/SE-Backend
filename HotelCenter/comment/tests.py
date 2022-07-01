import http
import os
import io
import random
from datetime import timedelta, date
from django.utils.http import urlencode
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status, reverse

from HotelCenter.Hotel.models import Hotel


def my_reverse(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse.reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return f'{url}?{urlencode(query_kwargs)}'

    return url


class CommentTestCases(APITestCase):

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """

        self.test_root = os.path.abspath(os.path.dirname(__file__))
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        self.hotel_data1 = {
            "name": "parsian",
            "city": "Esfehan",
            "state": "Esfehan",
            "check_in_range": "9:00-12:00",
            "check_out_range": "15:00-23:00",
            "description": "good quality including breakfast",
            "phone_numbers": "09123456700",

            "facilities": [{"name": "free_wifi"}],
            "address": "Esfahan,Iran"
        }
        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "state": "mashhad",
            "check_in_range": "9:00-12:00",
            "check_out_range": "15:00-23:00",
            "description": "with best view of the city and places",
            "phone_numbers": "09123456709",
            'rate': 4.4,
            "facilities": [{"name": "free_wifi"}, {"name": "parking"}],
            "address": "Khorasan,Iran"
        }

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

    def test_comment_get_list(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})

    def test_comment_unauth(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})

    def test_comment__create_success(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})

    def test_comment__update_delete_wrong_auth(self):
        pass

    def test_comment__update_delete_create_hotel_not_valid(self):
        pass

    def test_comment__update_delete_success(self):
        pass

    def test_my_comment__unauth(self):
        url = my_reverse("hotel-mycomment-list", kwargs={"hid": 1})

    def test_my_comment__success(self):
        url = my_reverse("hotel-mycomment-list", kwargs={"hid": 1})
