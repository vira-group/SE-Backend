from django.test import TestCase

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase


class HotelTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create(is_active=True, email="nima.kam@gmail.com",
                                                     password="some-strong1pass")

    def test_hotel_creation(self):
        print(get_user_model().objects.get().password)
