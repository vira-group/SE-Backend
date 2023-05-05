from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from Account.models import Customer,Manager
from Hotel.models import Hotel
from rest_framework import status
from django.contrib.auth import get_user_model
import json


class NearHotel(APITestCase):
    def setUp(self) -> None:
                    new_user1 ={
                        "email": "amin@gmail.com",
                        "phone_number": "09133630096",
                        "role": "C",
                        "password": "ILOVEDJANGO"
    }
                    new_user2 ={
                        "email": "ali@gmail.com",
                        "phone_number": "09133630095",
                        "role": "M",
                        "password": "ILOVEDJANGO"
    }
                    
                    new_user3 ={
                        "email": "reza@gmail.com",
                        "phone_number": "09133630092",
                        "role": "A",
                        "password": "ILOVEDJANGO"
    }
                    
                    
    
                    hotel_data1 = {
                            "name": "Parsian",
                            "phone_number": "0912345678",
                            "description": "Nice Hotel",
                            "country": "Iran",
                            "city": "Esfahan",
                            "longitude": 2,
                            "latitude": 1,
                            "address": "Esfahan, Iran"
                            }
                        
                    hotel_data2 = {
                            "name": "Ferdosi",
                            "city": "Khorasan",
                            "country": "Iran",
                            "check_in": "15:00",
                            "check_out": "12:00",
                            "description": "with best view of the city and places",
                            "phone_number": "09123456709",
                            'rate': 4.4,
                            "address": "Khorasan,Iran",
                            "longitude": 0.25,
                            "latitude": 0.25,
                        }
                    hotel_data3 = {
                            "name": "amirkabir",
                            "city": "Kashan",
                            "country": "Iran",
                            "check_in": "15:00",
                            "check_out": "12:00",
                            "description": "with best view of the city and places",
                            "phone_number": "09132001683",
                            'rate': 4.4,
                            "address": "Khorasan,Iran",
                            "longitude": 0.1,
                            "latitude": 0.1,
                        }
                    
                    self.myloc1={"x":0, "y":0}
                    self.myloc2={"x":0.25, "y":0.25}
                    self.myloc3={"x":1, "y":1}
                    

                    
                    self.user1 =get_user_model().objects.create_user(**new_user1)
                    self.user1.is_active=True
                    self.user1.save()
                    self.token1 = Token.objects.create(user=self.user1)
                    
                    
                    
                    self.user2 =get_user_model().objects.create_user(**new_user2)
                    self.user2.is_active=True
                    self.user2.save()
                    self.token2 = Token.objects.create(user=self.user2)
                    
                    
                    self.user3 =get_user_model().objects.create_user(**new_user3)
                    self.user3.is_active=True
                    self.user3.save()
                    self.token3 = Token.objects.create(user=self.user3)
                    
                    self.h1=Hotel.objects.create(manager=self.user2,**hotel_data1)
                    self.h2=Hotel.objects.create(manager=self.user2,**hotel_data2)
                    self.h3=Hotel.objects.create(manager=self.user2,**hotel_data3)
                    
                    
                    
    def set_credential(self, token):
            """
                set token for authorization
            """
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_is_not_None(self):
        # request1=self.client.get(reverse("nearhotel"),self.myloc1).json()
        # request2=self.client.get(reverse("nearhotel"),self.myloc2).json()
        # request3=self.client.get(reverse("nearhotel"),self.myloc3).json()
        
        # self.assertNotEqual(request1,None)
        # self.assertNotEqual(request2,None)
        # self.assertNotEqual(request3,None)
        pass 
    def test_result(self):
        
        request1=self.client.get(reverse("nearhotel"),self.myloc1).json()
        request2=self.client.get(reverse("nearhotel"),self.myloc2).json()
        request3=self.client.get(reverse("nearhotel"),self.myloc3).json()
        
        self.assertEqual({2,3},{i["id"] for i in request1})
        self.assertEqual({2,3},{i["id"] for i in request2})
        self.assertEqual({3,1},{i["id"] for i in request3})
        