from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class HotelTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create(is_active=True, email="nima.kam@gmail.com")
        self.user1.set_password("some-strong1pass")
        self.user1.save()

        self.user2 = get_user_model().objects.create(is_active=True, email="mohammad@gmail.com")
        self.user2.set_password("some-strong2pass")
        self.user2.save()

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def test_hotel_creation(self):
        print(get_user_model().objects.get(pk=2).password)
        res = self.client.post("/auth/users/", data={"email": "koxigat465@snece.com",
                                                                  "password": "nima1234", "re_password": "nima1234"})
        print(res.status_code, "\n", res.content)
