from django.test import TestCase

from rest_framework import status, reverse
from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from Hotel.models import Hotel , Facility



class chatTestCase(APITestCase):
    test_urls = {
        "user-chatlist": '/api/chat/mychatlist/',
        "hotel_chatlist": '/api/chat/hotelcahtlist/{}/'
    }

    def setUp(self) -> None:
        """
            RUNS BEFORE EACH TEST
        """
        self.facility1 = {"name": "free_wifi"}
        self.facility2 = {"name": "parking"}

        Facility.objects.create(**self.facility1)
        Facility.objects.create(**self.facility2)

        self.hotel_data1 = {
            "name": "parsian",
            "city": "Esfehan",
            "state": "Esfehan",
            "country": "Iran",
            "description": "good quality including breakfast",
            "phone_numbers": "09123456700",

            "facilities": [{"name": "free_wifi"}],
            "address": "Esfahan,Iran"
        }

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
    
    def test_hotel_chatlist_success(self):
        self.hotel_data1.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
        self.set_credential(token=self.token1)
        response = self.client.get(self.test_urls["hotel_chatlist"].format(hotel1.id))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_hotel_chatlist_unauthorized(self):
        self.hotel_data1.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
        self.unset_credential()
        response = self.client.get(self.test_urls["hotel_chatlist"].format(hotel1.id))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_hotel_chatlist_not_hotel_creator_or_editor(self):
        self.hotel_data1.pop("facilities")
        hotel1 = Hotel.objects.create(**self.hotel_data1, creator_id=self.user1.id)
        self.set_credential(token=self.token2)
        response = self.client.get(self.test_urls["hotel_chatlist"].format(hotel1.id))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)