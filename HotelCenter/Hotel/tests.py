import http
from django.test import TestCase
import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Hotel


class HotelTestCase(APITestCase):
    test_urls = {
        "hotel-list": "/hotel/hotels/",
        "hotel-obj": "/hotel/hotels/{}/",
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """
        self.hotel_data1 = {
            "name": "parsian",
            "city": "Esfehan",
            "state": "Esfehan",
            "description": "good quality including breakfast",
            "phone_numbers": "09123456700",
            "facilities": [{"name": "free_wifi"}]
        }

        self.user1 = get_user_model().objects.create(is_active=True, email="nima.kam@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(is_active=True, email="mohammad@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

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

    def test_hotel_creation_success(self):
        # create hotel for user1
        self.set_credential(token=self.token1)
        current_count = Hotel.objects.count()
        data = self.hotel_data1

        resp = self.client.post(self.test_urls["hotel-list"], data=data, format="json")
        content = resp.data

        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(content["name"], data["name"])
        self.assertTrue(Hotel.objects.count() == current_count + 1)

        # each person can have only one hotel
        resp = self.client.post(self.test_urls["hotel-list"], data=data, format="json")
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)
        self.assertTrue(Hotel.objects.count() == current_count + 1)

        data["name"] = "old parsian"
        resp = self.client.put(self.test_urls["hotel-obj"].format(1), data=data, format="json")
        # print(resp.data)
        content = resp.data

        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(content["name"], data["name"])
        self.assertTrue(Hotel.objects.count() == current_count + 1)

    def test_hotel_creation_miss_fields(self):
        self.set_credential(token=self.token1)
        current_count = Hotel.objects.count()
        data = self.hotel_data1
        data.pop("city")

        resp = self.client.post(self.test_urls["hotel-list"], data=data, format="json")
        content = resp.data
        # print(content, "\n miss: ", resp.status_code)

        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)
        # self.assertEqual(content["name"], data["name"])
        self.assertTrue(Hotel.objects.count() == current_count)

    def test_hotel_unauthorized(self):
        self.unset_credential()
        data = self.hotel_data1

        resp = self.client.post(self.test_urls["hotel-list"], data=data, format="json")

        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

        # resp = self.client.put(self.test_urls["hotel-obj"], data=data, format="json")
        #
        #
        # self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_hotel_retrieve(self):
        self.hotel_data1.pop("facilities")
        Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
        Hotel.objects.create(**self.hotel_data1, creator_id=self.user2.id)

        resp = self.client.get(self.test_urls["hotel-list"], format="json")

        content = resp.data
        self.assertTrue(resp.status_code == http.HTTPStatus.OK)
        self.assertTrue(len(content) == 2)

        resp = self.client.get(self.test_urls["hotel-obj"].format(1), format="json")
        content = resp.data
        self.assertTrue(resp.status_code == http.HTTPStatus.OK)
        self.assertTrue(content['name'] == self.hotel_data1['name'])
