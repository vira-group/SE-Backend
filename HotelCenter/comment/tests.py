import http
import os
import random
from datetime import timedelta, date
from django.utils.http import urlencode
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status, reverse

from Hotel.models import Hotel, Facility
from .models import Comment


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

        self.facility1 = Facility.objects.create(**self.facility1)
        self.facility2 = Facility.objects.create(**self.facility2)

        self.hotel_data1 = {
            "name": "parsian",
            "city": "Esfehan",
            "state": "Esfehan",
            "country": "Iran",
            "check_in_range": "9:00-12:00",
            "check_out_range": "15:00-23:00",
            "description": "good quality including breakfast",
            "phone_numbers": "09123456700",

            # "facilities": [{"name": "free_wifi"}],
            "address": "Esfahan,Iran"
        }
        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "state": "mashhad",
            "country": "Iran",
            "check_in_range": "9:00-12:00",
            "check_out_range": "15:00-23:00",
            "description": "with best view of the city and places",
            "phone_numbers": "09123456709",
            'rate': 4.4,
            # "facilities": [{"name": "free_wifi"}, {"name": "parking"}],
            "address": "Khorasan,Iran",

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

        self.hotel1 = Hotel.objects.create(creator=self.user2, **self.hotel_data1)
        self.hotel2 = Hotel.objects.create(creator=self.user2, **self.hotel_data2)

        self.comment1 = {
            "text": "The hotel was good and our room was clean.",
            "rate": 5
        }
        self.comment2 = {
            "text": "our room was dirty and there was no room services.",
            "rate": 2
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

    def create_comment(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})
        self.set_credential(self.token2)
        resp = self.client.post(url, data=self.comment1)

        self.set_credential(self.token1)
        resp = self.client.post(url, data=self.comment2)
        # comment2 = Comment.objects.create(**self.comment2, hotel=self.hotel1, writer=self.user1)
        resp = self.client.post(url, data=self.comment1)
        # comment2 = Comment.objects.create(**self.comment2, hotel=self.hotel1, writer=self.user1)

        url = my_reverse("hotel-comment-list", kwargs={"hid": 2})

        resp = self.client.post(url, data=self.comment1)
        # comment3 = Comment.objects.create(**self.comment1, hotel=self.hotel2, writer=self.user1)
        self.unset_credential()

    def test_comment_get_list(self):
        # not valid hotel
        url = my_reverse("hotel-comment-list", kwargs={"hid": 100})

        self.create_comment()

        resp = self.client.get(url)
        # print('1 comment list test resp: ', resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertTrue(len(resp.data) == 0)

        url = my_reverse("hotel-comment-list", kwargs={"hid": self.hotel1.id})

        resp = self.client.get(url)
        # print('1 comment list test resp: ', resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertTrue(len(resp.data) == 3)

    def test_comment_unauth(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})

        resp = self.client.post(url, data=self.comment1)
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_comment__create_success(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})
        self.set_credential(self.token1)
        # hotel1 = Hotel.objects.get(pk=1)
        resp = self.client.post(url, data=self.comment1)

        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)

        resp = self.client.post(url, data=self.comment2)
        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)

        resp = self.client.post(url, data=self.comment1)

        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)

        hotel1 = Hotel.objects.get(pk=1)
        self.assertTrue(hotel1.reply_count == 3)

    def test_comment__create_wrong_data(self):
        url = my_reverse("hotel-comment-list", kwargs={"hid": 1})
        self.set_credential(self.token1)

        data = {"text": "hi", "rate": "nine"}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"text": "hi", "rate": 9}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"text": "hi", "rate": -9}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"text": "hi"}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"rate": 5, "text": ""}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        url = my_reverse("hotel-comment-list", kwargs={"hid": 10})

        data = {"rate": 1, "text": "hotel did not exists"}
        resp = self.client.post(url, data=data)
        # print("test comment resp", resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)

    def test_comment__update_delete_wrong_auth(self):
        self.create_comment()
        url = my_reverse("hotel-comment-detail", kwargs={"pk": 1, "hid": 1})

        data = {"rate": 3}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

        self.set_credential(self.token3)
        data = {"rate": 4, "text": "hotel is updated"}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

        url = my_reverse("hotel-comment-detail", kwargs={"pk": 1, "hid": 20})

        self.set_credential(self.token1)
        data = {"rate": 4, "text": "hotel is updated"}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)

        url = my_reverse("hotel-comment-detail", kwargs={"pk": 1, "hid": 2})

        self.set_credential(self.token1)
        data = {"rate": 4, "text": "hotel is updated"}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)

    def test_comment__update_delete_hotel_not_valid(self):
        self.create_comment()
        self.set_credential(self.token2)
        url = my_reverse("hotel-comment-detail", kwargs={"pk": 1, "hid": 1})

        data = {"rate": 6}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

        data = {"rate": -4}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_comment__update_delete_success(self):
        self.create_comment()
        com=Comment.objects.filter(hotel=2).first()
        url = my_reverse("hotel-comment-detail", kwargs={"pk": com.id, "hid": 2})

        self.set_credential(self.token1)
        data = {"rate": 4, "text": "hotel is updated"}
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    def test_my_comment__unauth(self):
        self.create_comment()
        url = my_reverse("hotel-mycomment-list", kwargs={"hid": 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_my_comment__success(self):
        self.create_comment()
        url = my_reverse("hotel-mycomment-list", kwargs={"hid": 1})

        self.set_credential(self.token1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(len(resp.data), 2)
