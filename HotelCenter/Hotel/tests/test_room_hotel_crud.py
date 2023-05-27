import http
import os
import io
import random
from datetime import timedelta, date

from django.utils.datetime_safe import datetime
from rest_framework import status, reverse
from PIL import Image
from django.core.files import File
from django.http import HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.test import TestCase
import json
from django.utils.http import urlencode

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Hotel, HotelImage, Room, roomFacility, Reserve, FavoriteHotel


# def my_reverse(viewname, kwargs=None, query_kwargs=None):
#     """
#     Custom reverse to add a query string after the url
#     Example usage:
#     url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
#     """
#     url = reverse.reverse(viewname, kwargs=kwargs)

#     if query_kwargs:
#         return f'{url}?{urlencode(query_kwargs)}'

#     return url


class HotelTestCase(APITestCase):
    test_urls = {
        "hotel-list": "/api/hotel/create/",
        "hotel-obj": "/api/hotel/create/",
        # "hotel-images": "/api/hotel/{}/images/",
        # "hotel-image": "/api/hotel/{}/images/{}/",
        # "best-hotel": '/api/hotel/best/'
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """

        self.test_root = os.path.abspath(os.path.dirname(__file__))
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        self.hotel_data1 = {
            "name": "Parsian",
            "phone_number": "0912345678",
            "description": "Nice Hotel",
            "country": "Iran",
            "city": "Esfahan",
            "longitude": 0,
            "latitude": 0,
            "address": "Esfahan, Iran"
        }

        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "country": "Iran",
            "check_in": "15:00",
            "check_out": "12:00",
            "description": "with best view of the city and places",
            "phone_number": "09123456709",
            'rate': 4.4,
            "address": "Khorasan,Iran"
        }

        self.user1 = get_user_model().objects.create(
            is_active=True, email="user1@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.role = "M"
        self.user1.save()

        self.user2 = get_user_model().objects.create(
            is_active=True, email="user2@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.user3 = get_user_model().objects.create(
            is_active=True, email="user3@gmail.com")
        self.user3.set_password("some-strong3pass")
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

    # def generate_photo_file(self):
    #     file = io.BytesIO()
    #     r = random.Random().random()
    #     image = Image.new('RGB', size=(100, 100), color=(130, int(r * 120), int(10 + 5 * r)))
    #     file.name = './test.png'
    #     image.save("test.png", 'PNG')

    #     file.seek(0)
    #     return file

    def test_hotel_creation_success(self):
        # create hotel for user1
        self.set_credential(token=self.token1)
        current_count = Hotel.objects.count()
        self.hotel_data1['manager'] = self.user1.id
        data = self.hotel_data1

        resp = self.client.post(
            self.test_urls["hotel-list"], data=data, format="json")
        content = resp.data

        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(content["name"], data["name"])
        self.assertTrue(Hotel.objects.count() == current_count + 1)

        current_count = Hotel.objects.count()
        # each person can have more than one hotel
        self.hotel_data2['manager'] = self.user1.id
        data = self.hotel_data2

        resp = self.client.post(
            self.test_urls["hotel-list"], data=data, format="json")
        content = resp.data
        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)
        self.assertTrue(Hotel.objects.count() == current_count + 1)

        self.assertEqual(content["name"], data["name"])
        self.assertTrue(Hotel.objects.count() == current_count + 1)

    def test_hotel_creation_miss_fields(self):

        self.set_credential(token=self.token1)
        current_count = Hotel.objects.count()
        data = self.hotel_data1
        data.pop("city")

        resp = self.client.post(
            self.test_urls["hotel-list"], data=data, format="json")
        content = resp.data

        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)
        self.assertTrue(Hotel.objects.count() == current_count)

    def test_hotel_unauthorized(self):

        self.unset_credential()
        data = self.hotel_data1
        self.hotel_data1['manager'] = self.user1.id

        resp = self.client.post(
            self.test_urls["hotel-list"], data=data, format="json")
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

        resp = self.client.post(
            self.test_urls["hotel-obj"], data=data, format="json")
        self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    def test_hotel_retrieve(self):

        Hotel.objects.create(**self.hotel_data2, manager_id=self.user2.id)

        resp = self.client.get(self.test_urls["hotel-list"], format="json")

        content = resp.data
        self.assertTrue(resp.status_code == http.HTTPStatus.OK)
        self.assertTrue(len(content) == 1)

        resp = self.client.get(
            self.test_urls["hotel-obj"].format(1), format="json")
        content = resp.data
        self.assertTrue(resp.status_code == http.HTTPStatus.OK)
        self.assertTrue(content[0]['name'] == self.hotel_data2['name'])

    # def test_Hotel_header_set(self):
    #     self.hotel_data2.pop("facilities")
    #     hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user1.id)
    #     self.set_credential(self.token1)

    #     imag = self.generate_photo_file()

    #     with open(imag.name, 'rb') as img:
    #         # print("hotel header type:", img.read())
    #         data = {
    #             "image": img
    #         }
    #         resp: HttpResponseBadRequest = self.client.post(
    #             self.test_urls['hotel-images'].format(hotel1.id) + '?is_header=true', data,
    #             format='multipart')

    #     # print("in header test : ", resp)
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    # def test_Hotel_image_UnAuthorized(self):  #
    #     self.hotel_data2.pop("facilities")
    #     hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=1)
    #     resp = self.client.post(self.test_urls['hotel-images'].format(1))
    #     self.assertTrue(resp.status_code == http.HTTPStatus.UNAUTHORIZED)
    #     imag = self.generate_photo_file()

    #     with open(imag.name, 'rb') as img:
    #         data = {
    #             "image": img
    #         }
    #         resp = self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

    #     self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    #     # wrong permission
    #     self.set_credential(self.token3)
    #     # print("permission\n\n", resp.status_code, 'data ', resp.data)
    #     with open(imag.name, 'rb') as img:
    #         # print("hotel header type:", img.read())
    #         data = {
    #             "image": img
    #         }
    #         self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

    #     self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    # def test_Invalide_image(self):  # ***
    #     self.hotel_data2.pop("facilities")
    #     hotel1 = Hotel.objects.create(**self.hotel_data2, creator_id=1)
    #     self.set_credential(self.token1)

    #     tex = open('text1.txt', 'w')
    #     tex.close()

    #     with open('text1.txt') as txt:
    #         resp = self.client.post(self.test_urls['hotel-images'].format(hotel1.id), data={"image": txt})
    #     # print("invalid\n\n", resp.status_code, 'data ', resp.data)
    #     self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)
    #     # self.client.post(self.test_urls['hotel-images'].format(1))

    # def test_Best_New_hotel_list(self):  # ***
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

    #     resp = self.client.get(path=self.test_urls['best-hotel'])
    #     self.assertEqual(resp.status_code, 200)
    #     # print("resp: best hotel", resp.data)
    #     for i in range(1, len(resp.data)):
    #         self.assertTrue(resp.data[i - 1]['rate'] >= resp.data[i]['rate'])

    #     resp = self.client.get(path=my_reverse("best-hotel-list", query_kwargs={"count": 2}))
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    #     self.assertTrue(len(resp.data) <= 2)

    #     resp = self.client.get(my_reverse("new-hotel-list"))
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    #     self.assertTrue(len(resp.data) == 3)

    # def test_Delete_hotel_img(self):  # ***
    #     self.hotel_data1.pop("facilities")
    #     hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)

    #     imag = self.generate_photo_file()

    #     # data = {
    #     #     "image": img
    #     # }
    #     self.set_credential(self.token1)
    #     count = HotelImage.objects.count()
    #     # './test_img/img1.jpg'
    #     with open(imag.name, 'rb') as img:
    #         # print("hotel header type:", img.read())
    #         data = {
    #             "image": img
    #         }
    #         resp = self.client.post(self.test_urls['hotel-images'].format(1), data, format='multipart')

    #     # print("\nimage created", count)
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     count2 = HotelImage.objects.count()

    #     self.assertTrue(count2 == count + 1)

    #     image1 = HotelImage.objects.last()
    #     resp = self.client.delete(self.test_urls['hotel-image'].format(hotel1.id, image1.id))
    #     self.assertEqual(resp.status_code, http.HTTPStatus.NO_CONTENT)
    #     count3 = HotelImage.objects.count()

    #     self.assertTrue(count3 == count2 - 1)

    def test_my_hotels_noauth(self):

        resp = self.client.post(reverse.reverse('my_hotels-list'))
        self.assertEqual(http.HTTPStatus.UNAUTHORIZED, resp.status_code)
        resp = self.client.get(reverse.reverse('my_hotels-list'))
        self.assertEqual(http.HTTPStatus.UNAUTHORIZED, resp.status_code)

    def test_my_hotels_success(self):
        hotel_data3 = self.hotel_data2.copy()
        hotel_data3['rate'] = 3.9
        hotel1: Hotel = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        hotel2: Hotel = Hotel.objects.create(
            **self.hotel_data2, manager_id=self.user2.id)
        hotel3: Hotel = Hotel.objects.create(
            **hotel_data3, manager_id=self.user3.id)
        hotel2.save()
        hotel3.save()

        self.set_credential(self.token1)

        resp = self.client.get(reverse.reverse('my_hotels-list'))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertTrue((len(resp.data['managers']) == 1))

    # def test_favorite_hotel_unauthorized(self):
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     hotel1: Hotel = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     hotel2: Hotel = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     hotel3: Hotel = Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

    #     # self.set_credential(self.token1)
    #     resp = self.client.get(my_reverse('favorite_hotels-list'))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    #     resp = self.client.post(my_reverse('favorite_hotels-list'))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

    # def test_favorite_hotel_add_invalid_hotel(self):
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     hotel1: Hotel = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     hotel2: Hotel = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     hotel3: Hotel = Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

    #     self.set_credential(self.token1)
    #     data = {
    #         "hotel": 1
    #     }
    #     resp = self.client.post(my_reverse('favorite_hotels-list'), data=data)  # hotel_id not send

    #     self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

    #     data = {
    #         "hotel_id": 1000
    #     }
    #     resp = self.client.post(my_reverse('favorite_hotels-list'), data=data)  # hotel_id Not exist

    #     self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)

    # def test_favorite_hotel_add_success(self):
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     hotel1: Hotel = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     hotel2: Hotel = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     hotel3: Hotel = Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

    #     self.set_credential(self.token1)
    #     data = {
    #         "hotel_id": 2
    #     }
    #     resp = self.client.post(my_reverse('favorite_hotels-list'), data=data)
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    #     data = {
    #         "hotel_id": 3
    #     }
    #     resp = self.client.post(my_reverse('favorite_hotels-list'), data=data)

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    #     resp = self.client.get(my_reverse('favorite_hotels-list'))
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 2)

    #     data = {
    #         "hotel_id": 2
    #     }
    #     resp = self.client.post(my_reverse('favorite_hotels-list'), data=data)

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    #     resp = self.client.get(my_reverse('favorite_hotels-list'))
    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 1)

    # def test_favorite_hotel_list_success(self):
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     hotel1: Hotel = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     hotel2: Hotel = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     hotel3: Hotel = Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)

    #     self.set_credential(self.token1)
    #     FavoriteHotel.objects.create(user=self.user1, hotel=hotel1)
    #     FavoriteHotel.objects.create(user=self.user1, hotel=hotel2)
    #     FavoriteHotel.objects.create(user=self.user1, hotel=hotel3)

    #     resp = self.client.get(my_reverse('favorite_hotels-list'))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 3)


class RoomTestCase(APITestCase):
    test_urls = {
        "add_room": '/api/hotel/room/{}/',
        "get_hotel_rooms": '/api/hotel/room/{}',
        "add_room_image": '/api/hotel/room/{}/images/'
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        self.roomfacility1 = {"name": "rf1"}
        self.roomfacility2 = {"name": "rf2"}

        roomFacility.objects.create(**self.roomfacility1)
        roomFacility.objects.create(**self.roomfacility2)

        self.hotel_data1 = {
            "name": "Parsian",
            "phone_number": "0912345678",
            "description": "Nice Hotel",
            "country": "Iran",
            "city": "Esfahan",
            "longitude": 0,
            "latitude": 0,
            "address": "Esfahan, Iran"
        }

        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "country": "Iran",
            "check_in": "15:00",
            "check_out": "12:00",
            "description": "with best view of the city and places",
            "phone_number": "09123456709",
            'rate': 4.4,
            "address": "Khorasan,Iran"
        }

        self.room_data1 = {
            "type": "Standard Double Room",
            "view": "no view",
            "capacity": "2",
            "price": "20000",
        }
        self.room_data2 = {
            "type": "Single Bed Room",
            "view": "sea",
            "capacity": 1,
            'size': 1,
            "price": "15000",
        }

        self.user1 = get_user_model().objects.create(
            is_active=True, email="hediyeh@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(
            is_active=True, email="hediyeh1@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.user3 = get_user_model().objects.create(
            is_active=True, email="hediyeh3@gmail.com")
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

    def test_room_creation_success(self):
        # create hotel for user1
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        self.set_credential(self.token1)
        resp = self.client.post(
            self.test_urls['add_room'].format(hotel1.id), self.room_data1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_room_creation_unauthorized(self):
        # create hotel for user1
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        resp = self.client.post(
            self.test_urls['add_room'].format(hotel1.id), self.room_data1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_room_imgae(self):
        hotel1 = Hotel.objects.create(**self.hotel_data1, manager_id=self.user1.id)
        self.set_credential(self.token1)
        resp = self.client.post(self.test_urls['add_room'].format(hotel1.id), self.room_data1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        imag = self.generate_photo_file()

        with open(imag.name, 'rb') as img:
            data = {
                "image": img
            }
            resp: HttpResponseBadRequest = self.client.post(
                self.test_urls['add_room_image'].format(Room.objects.filter(hotel=hotel1)[0].id), data,
                format='multipart')
        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)

    def test_Invalide_room_image(self):
        hotel1 = Hotel.objects.create(**self.hotel_data1, manager_id=self.user1.id)
        self.set_credential(self.token1)
        resp = self.client.post(self.test_urls['add_room'].format(hotel1.id), self.room_data1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        tex = open('text1.txt', 'w')
        tex.close()

        with open('text1.txt') as txt:
            resp = self.client.post(self.test_urls['add_room_image'].format(hotel1.id), data={"image": txt})
        self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_room_image_Failed(self):
        hotel1 = Hotel.objects.create(**self.hotel_data1, manager_id=self.user1.id)
        resp = self.client.post(self.test_urls['add_room'].format(hotel1.id), self.room_data1)
        imag = self.generate_photo_file()
        with open(imag.name, 'rb') as img:
            data = {
                "image": img
            }
            resp = self.client.post(self.test_urls['add_room_image'].format(1), data, format='multipart')
        self.assertEqual(resp.status_code, 404)
        self.set_credential(self.token3)
        with open(imag.name, 'rb') as img:
            data = {
                "image": img
            }
            self.client.post(self.test_urls['add_room_image'].format(1), data, format='multipart')

        self.assertEqual(resp.status_code, 404)

    # def test_room_search(self):
    #     self.hotel_data1.pop("facilities")
    #     self.hotel_data2.pop("facilities")
    #     hotel_data3 = self.hotel_data2.copy()
    #     hotel_data3['rate'] = 3.9
    #     hotel1: Hotel = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
    #     hotel2: Hotel = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
    #     hotel3: Hotel = Hotel.objects.create(**hotel_data3, creator_id=self.user3.id)
    #     # hotel2.editors.add(self.user1)
    #     # hotel2.save()
    #     # hotel3.editors.add(self.user1)
    #     # hotel3.save()
    #     self.room_data1.pop("room_facilities")
    #     self.room_data2.pop("room_facilities")
    #     room3 = self.room_data1.copy()
    #     room3['sleeps'] = 3
    #     room3['size'] = 3

    #     Room.objects.create(hotel=hotel1, **self.room_data2)
    #     Room.objects.create(hotel=hotel1, **self.room_data1, size=2)
    #     Room.objects.create(hotel=hotel1, **room3)

    #     self.set_credential(self.token1)
    #     # print(my_reverse("hotel-room-search-list", kwargs={"hid": 1}, query_kwargs={'size': 2}))
    #     resp = self.client.get(reverse.reverse("hotel-room-search-list", kwargs={"hid": 1}))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 3)

    #     resp = self.client.get(my_reverse("hotel-room-search-list", kwargs={"hid": 1}, query_kwargs={'size': 2}))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 2)

    #     resp = self.client.get(my_reverse("hotel-room-search-list", kwargs={"hid": 1},
    #                                       query_kwargs={'size': 2, "check_in": datetime.today().date()}))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.BAD_REQUEST)

    #     resp = self.client.get(my_reverse("hotel-room-search-list", kwargs={"hid": 1},
    #                                       query_kwargs={'size': 2, "check_in": '2022-10-12',
    #                                                     "check_out": '2022-10-14'}))

    #     self.assertEqual(resp.status_code, http.HTTPStatus.OK)
    #     self.assertEqual(len(resp.data), 0)


class ReserveTestCase(APITestCase):
    test_urls = {
        "reserve_room": '/api/hotel/reserve/room/{}/',
        "user_reserve_list": '/api/hotel/reserve',
        # "roomspace_reservation_list": '/api/hotel/reserve/roomspace/{}/'
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        roomFacility.objects.create(**self.facility1)
        roomFacility.objects.create(**self.facility2)

        self.hotel_data1 = {
            "name": "Parsian",
            "phone_number": "0912345678",
            "description": "Nice Hotel",
            "country": "Iran",
            "city": "Esfahan",
            "longitude": 0,
            "latitude": 0,
            "address": "Esfahan, Iran"
        }

        self.hotel_data2 = {
            "name": "Ferdosi",
            "city": "Khorasan",
            "country": "Iran",
            "check_in": "15:00",
            "check_out": "12:00",
            "description": "with best view of the city and places",
            "phone_number": "09123456709",
            'rate': 4.4,
            "address": "Khorasan,Iran"
        }

        self.room_data1 = {
            "type": "Standard Double Room",
            "view": "no view",
            "capacity": "2",
            "price": "20000",
        }

        self.user1 = get_user_model().objects.create(
            is_active=True, email="hediyeh@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(
            is_active=True, email="hediyeh1@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.user3 = get_user_model().objects.create(
            is_active=True, email="hediyeh3@gmail.com")
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

    def test_reserve_success(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        self.user1.balance = 1000000
        self.user1.save()
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() + timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_reserve_not_enough_credit(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() + timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_reserve_invalid_date_pastdate(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        data = {
            "check_in": datetime.today().date() - timedelta(days=4),
            "check_out": datetime.today().date() + timedelta(days=2),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reserve_invalid_date_end_before_start(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() - timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reserve_invalid_room(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() + timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 2,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_reserve_unauthorized(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.unset_credential()
        self.user1.balance = 1000000
        self.user1.save()
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() + timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00989199999999"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reserve_invalid_phone_number(self):
        hotel1 = Hotel.objects.create(
            **self.hotel_data1, manager_id=self.user1.id)
        room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
        self.set_credential(token=self.token1)
        self.user1.balance = 1000000
        self.user1.save()
        data = {
            "check_in": datetime.today().date() + timedelta(days=1),
            "check_out": datetime.today().date() + timedelta(days=3),
            "firstname": "fn",
            "lastname": "ln",
            "room_id": 1,
            "adults": 2,
            "children": 0,
            "phone_number": "00000000000000000000000000000000000000000000000000000000000000000000000000000000"
        }
        response = self.client.post(
            self.test_urls["reserve_room"].format(room1.id), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


# class AdminTestCase(APITestCase):

#     def setUp(self) -> None:
#         """
#             RUNS BEFORE EACH TEST
#         """
#         self.facility1 = {"name": "free_wifi"}
#         self.facility2 = {"name": "parking"}

#         Facility.objects.create(**self.facility1)
#         Facility.objects.create(**self.facility2)

#         self.hotel_data1 = {
#             "name": "parsian",
#             "city": "Esfehan",
#             "state": "Esfehan",
#             "country": "Iran",
#             "description": "good quality including breakfast",
#             "phone_numbers": "09123456700",

#             "facilities": [{"name": "free_wifi"}],
#             "address": "Esfahan,Iran"
#         }
#         self.hotel_data2 = {
#             "name": "Ferdosi",
#             "city": "Khorasan",
#             "state": "mashhad",
#             "country": "Iran",
#             "description": "with best view of the city and places",
#             "phone_numbers": "09123456709",
#             'rate': 4.4,
#             "facilities": [{"name": "free_wifi"}, {"name": "parking"}],
#             "address": "Khorasan,Iran"
#         }

#         self.room_data1 = {
#             "type": "Standard Double Room",
#             "view": "no view",
#             "sleeps": "2",
#             "price": "10000",
#             "option": "free wifi",
#         }
#         self.room_data2 = {
#             "type": "King size Double bed Room",
#             "view": "city",
#             "sleeps": 3,
#             "price": "10000",
#             "option": "free wifi",
#         }

#         self.user1 = get_user_model().objects.create(is_active=True, email="hediyeh@gmail.com")
#         self.user1.set_password("some-strong1pass")
#         self.user1.save()

#         self.user2 = get_user_model().objects.create(is_active=True, email="hediyeh1@gmail.com")
#         self.user2.set_password("some-strong2pass")
#         self.user2.save()

#         self.user3 = get_user_model().objects.create(is_active=True, email="hediyeh3@gmail.com")
#         self.user3.set_password("some-strong2pass")
#         self.user3.save()

#         self.token1 = Token.objects.create(user=self.user1)
#         self.token2 = Token.objects.create(user=self.user2)
#         self.token3 = Token.objects.create(user=self.user3)

#     def set_credential(self, token):
#         """
#             set token for authorization
#         """
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

#     def unset_credential(self):
#         """
#             unset existing headers
#         """
#         self.client.credentials()

#     def test_admin_panel_no_auth(self):
#         self.hotel_data1.pop("facilities")
#         self.hotel_data2.pop('facilities')
#         hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
#         hotel2 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
#         room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
#         room2 = Room.objects.create(**self.room_data2, hotel=hotel2)
#         roomspace1 = RoomSpace.objects.create(name="1", room=room1)
#         self.unset_credential()
#         self.user1.balance = 1000000
#         self.user1.save()

#         # No auth admin room
#         resp = self.client.get(my_reverse("hotel-admin-room-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

#         # No auth admin room space
#         resp = self.client.get(my_reverse("hotel-admin-roomspace-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

#         # No auth admin panel
#         resp = self.client.get(my_reverse("hotel-admin-panel-detail", {"pk": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.UNAUTHORIZED)

#     def test_admin_panel_wrong_auth(self):
#         self.hotel_data1.pop("facilities")
#         self.hotel_data2.pop('facilities')
#         hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
#         hotel2 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
#         room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
#         room2 = Room.objects.create(**self.room_data2, hotel=hotel2)
#         roomspace1 = RoomSpace.objects.create(name="1", room=room1)
#         self.set_credential(self.token3)
#         self.user1.balance = 1000000
#         self.user1.save()

#         # Wrong auth admin room
#         resp = self.client.get(my_reverse("hotel-admin-room-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

#         # Wrong auth admin room space
#         resp = self.client.get(my_reverse("hotel-admin-roomspace-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

#         # Wrong auth admin panel
#         data = {'date': datetime.today().date() - timedelta(days=1)}
#         resp = self.client.get(my_reverse("hotel-admin-panel-detail", {"pk": 1}), data)
#         # print('wrong auth test resp: ', resp.data)

#         self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)

#     def test_admin_panel_success(self):
#         self.hotel_data1.pop("facilities")
#         self.hotel_data2.pop('facilities')
#         hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
#         hotel2 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
#         room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
#         room2 = Room.objects.create(**self.room_data2, hotel=hotel2)
#         roomspace1 = RoomSpace.objects.create(name="1", room=room1)
#         self.set_credential(self.token1)
#         self.user1.balance = 1000000
#         self.user1.save()

#         # No data admin panel
#         # data = {'date': datetime.today().date() - timedelta(days=1)}
#         resp = self.client.get(my_reverse("hotel-admin-panel-detail", {"pk": 1}))  # , data)
#         # print(' auth test resp: ', resp.data)

#         self.assertEqual(resp.status_code, http.HTTPStatus.OK)

#         data = {'date': "r"}

#         # Wrong data admin panel
#         resp = self.client.get(my_reverse("hotel-admin-panel-detail", {"pk": 1}), data)
#         # print('wrong auth test resp: ', resp.data)

#         self.assertEqual(resp.status_code, http.HTTPStatus.OK)
#         data = {'date': date.today()}

#         # Wrong data admin panel
#         resp = self.client.get(my_reverse("hotel-admin-panel-detail", {"pk": 1}), data)
#         # print('wrong auth test resp: ', resp.data)

#         self.assertEqual(resp.status_code, http.HTTPStatus.OK)
#         self.assertEqual(resp.data['date'], data['date'])

#     def test_admin_panel_room_success(self):
#         self.hotel_data1.pop("facilities")
#         self.hotel_data2.pop('facilities')
#         hotel1 = Hotel.objects.create(**self.hotel_data1, creator=self.user1)
#         hotel2 = Hotel.objects.create(**self.hotel_data2, creator=self.user2)
#         room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
#         room2 = Room.objects.create(**self.room_data2, hotel=hotel2)
#         roomspace1 = RoomSpace.objects.create(name="1", room=room1)
#         self.set_credential(self.token1)
#         self.user1.balance = 1000000
#         self.user1.save()

#         # No data admin room
#         resp = self.client.get(my_reverse("hotel-admin-room-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.OK)

#     def test_admin_panel_room_space_success(self):
#         self.hotel_data1.pop("facilities")
#         self.hotel_data2.pop('facilities')
#         hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
#         hotel2 = Hotel.objects.create(**self.hotel_data2, creator_id=self.user2.id)
#         room1 = Room.objects.create(**self.room_data1, hotel=hotel1)
#         room2 = Room.objects.create(**self.room_data2, hotel=hotel2)
#         roomspace1 = RoomSpace.objects.create(name="1", room=room1)
#         self.set_credential(self.token1)
#         self.user1.balance = 1000000
#         self.user1.save()

#         # No data admin room space
#         resp = self.client.get(my_reverse("hotel-admin-roomspace-list", {"hid": 1}))

#         self.assertEqual(resp.status_code, http.HTTPStatus.OK)


# class CancelReserveTestCase(APITestCase):
#     test_urls = {
#         "cancel_reserve": '/api/hotel/cancelreserve/',
#     }

#     def setUp(self) -> None:
#         """
#             RUNS BEFORE EACH TEST
#         """
#         self.f1 = {"name": "free_wifi"}
#         self.f2 = {"name": "parking"}

#         Facility.objects.create(**self.f1)
#         Facility.objects.create(**self.f2)

#         self.hotel1 = {
#             "name": "parsian",
#             "city": "Esfehan",
#             "state": "Esfehan",
#             "description": "good quality including breakfast",
#             "phone_numbers": "09123456700",

#             "facilities": [{"name": "free_wifi"}],
#             "address": "Esfahan,Iran"
#         }
#         self.hotel2 = {
#             "name": "Ferdosi",
#             "city": "Khorasan",
#             "state": "mashhad",
#             "description": "with best view of the city and places",
#             "phone_numbers": "09123456709",
#             'rate': 4.4,
#             "facilities": [{"name": "free_wifi"}, {"name": "parking"}],
#             "address": "Khorasan,Iran"
#         }

#         self.room1 = {
#             "type": "Standard Double Room",
#             "view": "no view",
#             "sleeps": "2",
#             "price": "10000",
#             "option": "free wifi",
#         }

#         self.u1 = get_user_model().objects.create(is_active=True, email="hediyeh@gmail.com")
#         self.u1.set_password("some-strong1pass")
#         self.u1.save()

#         self.u2 = get_user_model().objects.create(is_active=True, email="hediyeh1@gmail.com")
#         self.u2.set_password("some-strong2pass")
#         self.u2.save()

#         self.u3 = get_user_model().objects.create(is_active=True, email="hediyeh3@gmail.com")
#         self.u3.set_password("some-strong2pass")
#         self.u3.save()

#         self.t1 = Token.objects.create(user=self.u1)
#         self.t2 = Token.objects.create(user=self.u2)
#         self.t3 = Token.objects.create(user=self.u3)

#     def set_credential(self, token):
#         """
#             set token for authorization
#         """
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

#     def unset_credential(self):
#         """
#             unset existing headers
#         """
#         self.client.credentials()

#     def test_cancel_reserve_success(self):
#         self.hotel1.pop("facilities")
#         h1 = Hotel.objects.create(**self.hotel1, creator_id=self.u1.id)
#         room1 = Room.objects.create(**self.room1, hotel=h1)
#         roomspace = RoomSpace.objects.create(name="roomspace1", room=room1)
#         self.set_credential(token=self.t1)
#         self.u1.balance = 1000000
#         self.u1.save()
#         data = {
#             "check_in": datetime.today().date() + timedelta(days=1),
#             "check_out": datetime.today().date() + timedelta(days=3),
#             "firstname": "fn",
#             "lastname": "ln",
#             "room": room1,
#             "price_per_day": 5,
#             "national_code": "00",
#             "phone_number": "09199999999",
#             "roomspace_id": roomspace.id
#         }
#         reserve = Reserve.objects.create(**data, user=self.u1)
#         data = {
#             "reserve": reserve.id
#         }
#         response = self.client.post(self.test_urls["cancel_reserve"], data)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)

#     def test_cancel_reserve_unauthorized(self):
#         self.hotel1.pop("facilities")
#         h1 = Hotel.objects.create(**self.hotel1, creator_id=self.u1.id)
#         room1 = Room.objects.create(**self.room1, hotel=h1)
#         roomspace = RoomSpace.objects.create(name="roomspace1", room=room1)
#         self.unset_credential()
#         self.u1.balance = 1000000
#         self.u1.save()
#         data = {
#             "check_in": datetime.today().date() + timedelta(days=1),
#             "check_out": datetime.today().date() + timedelta(days=3),
#             "firstname": "fn",
#             "lastname": "ln",
#             "room": room1,
#             "price_per_day": 5,
#             "national_code": "00",
#             "phone_number": "09199999999",
#             "roomspace_id": roomspace.id
#         }
#         reserve = Reserve.objects.create(**data, user=self.u1)
#         data = {
#             "reserve": reserve.id
#         }
#         response = self.client.post(self.test_urls["cancel_reserve"], data)
#         self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_cancel_reserve_not_in_user_reserves(self):
#         self.hotel1.pop("facilities")
#         h1 = Hotel.objects.create(**self.hotel1, creator_id=self.u1.id)
#         room1 = Room.objects.create(**self.room1, hotel=h1)
#         roomspace = RoomSpace.objects.create(name="roomspace1", room=room1)
#         self.set_credential(self.t1)
#         self.u1.balance = 1000000
#         self.u1.save()
#         data = {
#             "check_in": datetime.today().date() + timedelta(days=1),
#             "check_out": datetime.today().date() + timedelta(days=3),
#             "firstname": "fn",
#             "lastname": "ln",
#             "room": room1,
#             "price_per_day": 5,
#             "national_code": "00",
#             "phone_number": "09199999999",
#             "roomspace_id": roomspace.id
#         }
#         reserve = Reserve.objects.create(**data, user=self.u2)
#         data = {
#             "reserve": reserve.id
#         }
#         response = self.client.post(self.test_urls["cancel_reserve"], data)
#         self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_cancel_reserve_for_past_time(self):
#         self.hotel1.pop("facilities")
#         h1 = Hotel.objects.create(**self.hotel1, creator_id=self.u1.id)
#         room1 = Room.objects.create(**self.room1, hotel=h1)
#         roomspace = RoomSpace.objects.create(name="roomspace1", room=room1)
#         self.set_credential(token=self.t1)
#         self.u1.balance = 1000000
#         self.u1.save()
#         data = {
#             "check_in": datetime.today().date() - timedelta(days=3),
#             "check_out": datetime.today().date() - timedelta(days=1),
#             "firstname": "fn",
#             "lastname": "ln",
#             "room": room1,
#             "price_per_day": 5,
#             "national_code": "00",
#             "phone_number": "09199999999",
#             "roomspace_id": roomspace.id
#         }
#         reserve = Reserve.objects.create(**data, user=self.u1)
#         data = {
#             "reserve": reserve.id
#         }
#         response = self.client.post(self.test_urls["cancel_reserve"], data)
#         self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
