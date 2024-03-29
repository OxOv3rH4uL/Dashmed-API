from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

class BookTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"name": "Test", "email": "test@gmail.com", "password": "test123"}
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_date": "1925-04-10",
            "isbn": "987-654-3298",
            "description": "Test Description"
        }
        self.updated_book_data = {
            "title": "Test Book Updated",
            "author": "Test Author",
            "publication_date": "1925-04-10",
            "isbn": "987-654-3298",
            "description": "Test Description Updated"
        }
        self.jwt_token = None
    
    def register_and_login_user_01(self):
        response = self.client.post("http://localhost:8000/user/register", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post("http://localhost:8000/user/login", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jwt_token', response.cookies)
        self.jwt_token = response.cookies['jwt_token'].value
    

    def test_add_book_02(self):
        self.client.cookies['jwt_token'] = self.jwt_token  
        response = self.client.post("http://localhost:8000/api/books/", self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Book Added Successfully!")
    
    def test_get_books_03(self):
        self.test_add_book_02()
        self.client.cookies['jwt_token'] = self.jwt_token
        response = self.client.get("http://localhost:8000/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(content['results']),0)
    
    def test_get_single_book_04(self):
        self.test_add_book_02()
        self.client.cookies['jwt_token'] = self.jwt_token
        response = self.client.get("http://localhost:8000/api/books/"+self.book_data['isbn']+"/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(content),1)
        self.assertEqual(content,self.book_data)
    
    def test_update_book_05(self):
        self.test_add_book_02()
        self.client.cookies['jwt_token'] = self.jwt_token
        response = self.client.put("http://localhost:8000/api/books/"+self.book_data['isbn']+"/",self.updated_book_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'],"Updated Successfully!")
        self.assertEqual(content['data'],self.updated_book_data)
    
    def test_delete_book(self):
        self.test_add_book_02()
        self.client.cookies['jwt_token'] = self.jwt_token
        response = self.client.delete("http://localhost:8000/api/books/"+self.book_data['isbn']+'/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'],"Book deleted successfully")
        response = self.client.get("http://localhost:8000/api/books/"+self.book_data['isbn']+'/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'],"Book Not Found!")


class FailureTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"name": "Test", "email": "test@gmail.com", "password": "test123"}
        self.book_data_1 = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "987-654-3298",
        }
        self.book_data_2 = {
            "title": "Test Book Duplicate",
            "author": "Test Author",
            "publication_date": "1925-04-10",
            "isbn": "987-654-3298",
            "description": "Test Description Duplicate"
        }
        self.incomplete_data = {
            "title": "Test Book Duplicate",
            "author": "Test Author",
            "publication_date": "1925-04-10"
        }
        self.invalid_data = {
            "title": "Test Book Invalid",
            "author": "Test Author",
            "publication_date": "3000-04-10",
            "isbn": "XXXXXXXXXXXX",
            "description": "Test Description Duplicate"
        }
        self.updated_book_data = {
            "title": "Test Book Updated",
            "author": "Test Author",
            "publication_date": "1925-04-10",
            "isbn": "987-654-3298",
            "description": "Test Description Updated"
        }
        self.jwt_token = None
        
    def test_not_authenticated_01(self):
        response = self.client.get("http://localhost:8000/api/books/")
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('jwt_token', response.cookies)
        self.assertEqual(content['message'],"User Not Authenticated. Head to /user/login")
    
    def register_and_login_user_02(self):
        response = self.client.post("http://localhost:8000/user/register", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post("http://localhost:8000/user/login", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jwt_token', response.cookies)
        self.jwt_token = response.cookies['jwt_token'].value
    
    
    def test_add_book_03(self):
        self.client.cookies['jwt_token'] = self.jwt_token  
        response = self.client.post("http://localhost:8000/api/books/", self.book_data_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Book Added Successfully!")
    
    def test_add_book_same_isbn_04(self):
        self.test_add_book_03()
        response = self.client.post("http://localhost:8000/api/books/",self.book_data_2)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message']['isbn'][0],"book with this isbn already exists.")
    
    def test_add_book_invalid_data_05(self):
        self.client.cookies['jwt_token'] = self.jwt_token  
        response = self.client.post("http://localhost:8000/api/books/", self.invalid_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_notfound_book_06(self):
        self.register_and_login_user_02()
        response = self.client.get("http://localhost:8000/api/books/"+self.invalid_data['isbn']+'/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Book Not Found!")
    
    def test_update_incomplete_detail_07(self):
        self.test_add_book_03()
        response = self.client.put("http://localhost:8000/api/books/"+self.book_data_1['isbn']+'/',self.incomplete_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Incomplete Details")
    
    def test_update_notfound_book_08(self):
        self.register_and_login_user_02()
        response = self.client.put("http://localhost:8000/api/books/"+self.book_data_1['isbn']+'/',self.updated_book_data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Book Not Found!")
    
    def test_delete_notfound_book_09(self):
        self.register_and_login_user_02()
        response = self.client.delete("http://localhost:8000/api/books/"+self.book_data_1['isbn']+'/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['message'], "Book Not Found!")


#Unit Testing Done








        



        
        
        

    



