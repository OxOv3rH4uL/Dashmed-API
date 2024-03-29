from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError,AuthenticationFailed
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer 
from .models import User
import datetime


class Register(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': "User Registered Successfully!"},status=status.HTTP_200_OK)
        except ValidationError as e:
            if 'unique' in str(e.detail):
                return Response({'error': 'Email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Registration Failed.', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    

class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'error':"User not found"},status=status.HTTP_404_NOT_FOUND)
        
        if user.password != password:
            return Response({'error':"Invalid Credentials. Please Try Again!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        data = {
            'id':user.id,
            'expiry': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
            'issued_at': datetime.datetime.now().isoformat()
        }

        token = jwt.encode(data,'secret',algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt_token',value=token,httponly=True)
        response.data = {
            "message":"Login Successful!"
        }

        return response

class Home(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt_token')

        if not token:
            return Response({"message":"User Not Authenticated"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"To start performing CRUD operations on the Library API, navigate to /libraryapi/books"},status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self,request):
        response = Response({"message":"Logout Successfull!"})
        response.delete_cookie('jwt_token')
        return response

class InvalidEndPoint(APIView):
    def get(self,request):
        return Response({"message":"Page not Found!"},status=status.HTTP_404_NOT_FOUND)

