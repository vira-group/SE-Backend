from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from Account.models import Customer,Manager
from rest_framework import status
from django.contrib.auth import get_user_model


class ProfileTest(APITestCase):
    
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
                 
    def set_credential(self, token):
        """
            set token for authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_user_cannot_show_profile(self):
        response =self.client.get(reverse("profile"))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_user_can_show_profile(self):
        self.set_credential(token=self.token1)
        response =self.client.get(reverse("profile"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_user_customer_first_profile_show(self):
        show_fisrt={
            'user': 
                {'phone_number': '09133630096',
                 'role': 'C', 
                 'email': 'amin@gmail.com'
                 },
                'first_name': 'cutomer1', 
                'last_name': 'customer_last_name', 
                'national_code': '',
                'gender': 'M'}
        self.set_credential(token=self.token1)
        response=self.client.get(reverse("profile"))
        self.assertEqual(response.json(),show_fisrt)
        self.assertNotEqual(response.json(),{})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_user_manager_first_profile_show(self):
        show_fisrt={
            'user': 
                {'phone_number': '09133630095',
                 'role': 'M', 
                 'email': 'ali@gmail.com'
                 },
                'name':f"Manager{self.user2.id}"
        }
        self.set_credential(token=self.token2)
        response=self.client.get(reverse("profile"))
        self.assertEqual(response.json(),show_fisrt)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_user_admin_first_profile_show(self):
        show_fisrt={
            'phone_number': '09133630092',
                 'role': 'A', 
                 'email': 'reza@gmail.com'
                 }
        self.set_credential(token=self.token3)
        response=self.client.get(reverse("profile"))
        self.assertEqual(response.json(),show_fisrt)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotEqual( response.json() ,{})

    def test_user_customer_empty_update_profile_show(self):
        show_fisrt={
            'user': 
                {'phone_number': '09133630096',
                 'role': 'C', 
                 'email': 'amin@gmail.com'
                 },
                'first_name': 'cutomer1', 
                'last_name': 'customer_last_name', 
                'national_code': '',
                'gender': 'M'}
        self.set_credential(token=self.token1)
        response=self.client.patch(reverse("profile"),{})
        self.assertEqual(response.json(),show_fisrt)
        self.assertNotEqual( response.json() ,{})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_user_manager_empty_profile_show(self):
        show_fisrt={
            'user': 
                {'phone_number': '09133630095',
                 'role': 'M', 
                 'email': 'ali@gmail.com'
                 },
                'name':f"Manager{self.user2.id}"
        }
        self.set_credential(token=self.token2)
        response=self.client.patch(reverse("profile"),{})
        self.assertEqual(response.json(),show_fisrt)
        self.assertNotEqual( response.json() ,{})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_user_admin_empty_update_profile_show(self):
        show_fisrt={
            'phone_number': '09133630092',
                 'role': 'A', 
                 'email': 'reza@gmail.com'
                 }
        self.set_credential(token=self.token3)
        response=self.client.patch(reverse("profile"),{})
        self.assertEqual(response.json(),show_fisrt)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotEqual( response.json() ,{})