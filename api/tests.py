from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {"username": "testing1234", "password": "testtinguser1234"}
        response = self.client.post("/register", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
        
    