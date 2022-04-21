import http
import os
import io
import random

from PIL import Image
from django.core.files import File
from django.http import HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.test import TestCase
import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Hotel, Facility, HotelImage


class HotelTestCase(APITestCase):
    test_urls = {
        "hotel-list": "/hotel/hotels/",
        "hotel-obj": "/hotel/hotels/{}/",
        "hotel-images": "/hotel/{}/images/",
        "hotel-image": "/hotel/{}/images/{}/",
        "best-hotel": '/hotel/best/'

    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """

        self.test_root = os.path.abspath(os.path.dirname(__file__))
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        Facility.objects.create(**self.facility1)
        Facility.objects.create(**self.facility2)

        self.hotel_data1 = {
            "name": "parsian",
            "city": "Esfehan",
            "state": "Esfehan",
            "description": "good quality including breakfast",
            "phone_numbers": "09123456700",

            "facilities": [{"name": "free_wifi"}],
            "address" : "Esfahan,Iran"
        }
        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "state": "mashhad",
            "description": "with best view of the city and places",
            "phone_numbers": "09123456709",
            'rate': 4.4,
            "facilities": [{"name": "free_wifi"}, {"name": "parking"}],
            "address" : "Khorasan,Iran"
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

    def generate_photo_file(self):
        file = io.BytesIO()
        r = random.Random().random()
        image = Image.new('RGB', size=(100, 100), color=(130, int(r * 120), int(10 + 5 * r)))
        file.name = './test.png'
        image.save("test.png", 'PNG')

        file.seek(0)
        return file

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

        resp = self.client.put(self.test_urls["hotel-obj"], data=data, format="json")

        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

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

    def test_Hotel_header_set(self):  # ***
        self.hotel_data2.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user1.id)
        self.set_credential(self.token1)

        imag = self.generate_photo_file()

        with open(imag.name, 'rb') as img:
            # print("hotel header type:", img.read())
            data = {
                "image": img
            }
            resp: HttpResponseBadRequest = self.client.post(
                self.test_urls['hotel-images'].format(hotel1.id) + '?is_header=true', data,
                format='multipart')

        # print("in header test : ", resp)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    def test_Hotel_image_UnAuthorized(self):  #
        self.hotel_data2.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=1)
        resp = self.client.post(self.test_urls['hotel-images'].format(1))
        self.assertTrue(resp.status_code == http.HTTPStatus.UNAUTHORIZED)
        imag = self.generate_photo_file()

        with open(imag.name, 'rb') as img:
            data = {
                "image": img
            }
            resp = self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

        # wrong permission
        self.set_credential(self.token3)
        # print("permission\n\n", resp.status_code, 'data ', resp.data)
        with open(imag.name, 'rb') as img:
            # print("hotel header type:", img.read())
            data = {
                "image": img
            }
            self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_Invalide_image(self):  # ***
        self.hotel_data2.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=1)
        self.set_credential(self.token1)

        tex = open('text1.txt', 'w')
        tex.close()

        with open('text1.txt') as txt:
            resp = self.client.post(self.test_urls['hotel-images'].format(hotel1.id), data={"image": txt})
        # print("invalid\n\n", resp.status_code, 'data ', resp.data)
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)
        # self.client.post(self.test_urls['hotel-images'].format(1))

    def test_Best_hotel_list(self):  # ***
        self.hotel_data1.pop("facilities")
        self.hotel_data2.pop("facilities")
        hotel_data3 = self.hotel_data2.copy()
        hotel_data3['rate'] = 3.9
        Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
        Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
        Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

        resp = self.client.get(path=self.test_urls['best-hotel'])
        self.assertEqual(resp.status_code, 200)
        # print("resp: best hotel", resp.data)
        for i in range(1, len(resp.data)):
            self.assertTrue(resp.data[i - 1]['rate'] >= resp.data[i]['rate'])

        resp = self.client.get(path=self.test_urls['best-hotel'] + "?count=2")
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(len(resp.data) <= 2)

    def test_Delete_hotel_img(self):  # ***
        self.hotel_data1.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)

        imag = self.generate_photo_file()

        # data = {
        #     "image": img
        # }
        self.set_credential(self.token1)
        count = HotelImage.objects.count()
        # './test_img/img1.jpg'
        with open(imag.name, 'rb') as img:
            # print("hotel header type:", img.read())
            data = {
                "image": img
            }
            resp = self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

        # print("\nimage created", count)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        count2 = HotelImage.objects.count()

        self.assertTrue(count2 == count + 1)

        image1 = HotelImage.objects.last()
        resp = self.client.delete(self.test_urls['hotel-image'].format(hotel1.id, image1.id))
        self.assertEqual(resp.status_code, http.HTTPStatus.NO_CONTENT)
        count3 = HotelImage.objects.count()

        self.assertTrue(count3 == count2 - 1)
