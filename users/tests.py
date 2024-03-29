from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import User
import json

class UserTestCase(TestCase):
    def setUp(self):
        self.client =  APIClient()

    def test_create_user(self):
        data = {"name":"Test","email":"test@gmail.com","password":"test123"}
        response = self.client.post("http://localhost:8000/user/register",data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(email=data['email']).exists(),True)
    
    def test_login_user(self):
        data = {"name":"Test","email":"test@gmail.com","password":"test123"}
        response = self.client.post("http://localhost:8000/user/register",data)
        data = {"email":"test@gmail.com","password":"test123"}
        response = self.client.post("http://localhost:8000/user/login",data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('jwt_token',response.cookies)
    
class FailureCases(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_failure_create_user(self):
        data = {"name":"Test","email":"test.gmail.com","password":"test123"}
        response = self.client.post("http://localhost:8000/user/register",data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=data['email']).exists(),False)
    
    def test_failure_login_user(self):
        data = {"email":"123@gmail.com","password":"test123"}
        response = self.client.post("http://localhost:8000/user/login",data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['error'], "User not found")



