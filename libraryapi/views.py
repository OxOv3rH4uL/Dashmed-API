from django.shortcuts import render
from .models import Book,Author
from .serializers import BookSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import json

class AddBook(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt_token')
        
        if token is not None:
            
            serializer = BookSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    
                    serializer.save()
                    return Response({'message':"Book Added Successfully!"},status=status.HTTP_201_CREATED)
            except ValidationError as e:
                
                if 'Name should contain only letters , spaces and dots.' in str(e.detail):
                    return Response({'message':"Name should contain only letters , spaces and dots."},status=status.HTTP_400_BAD_REQUEST)
                
                elif "Invalid ISBN format." in str(e.detail):
                    return Response({'message':"Invalid ISBN format. The ISBN should be in the format XXX-XXX-XXXX."},status=status.HTTP_400_BAD_REQUEST)
                
                elif "Publication Date Cannot be in future" in str(e.detail):
                    return Response({"message":"Publication Date Cannot be in Future."},status=status.HTTP_400_BAD_REQUEST)
                
                elif "Invalid date format. Date should be in YYYY-MM-DD format." in str(e.detail):
                    return Response({"message":"Invalid date format. Date should be in YYYY-MM-DD format."},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":e.detail},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':"User Not Authenticated. Head to /user/login"},status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self,request):
        token = request.COOKIES.get("jwt_token")
        print(token)
        if token is not None:
            book = Book.objects.all()
            serializers = BookSerializer(book,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"User Not Authenticated!"},status=status.HTTP_401_UNAUTHORIZED)


class GetBook(APIView):
    def get(self,request,isbn):
        token = request.COOKIES.get('jwt_token')
        # print(token)
        if token is not None:
            try:
                book = Book.objects.get(isbn=isbn)
                serializers = BookSerializer(book)
                return Response(serializers.data,status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                return Response({"message":"BooK Not Found!"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message":"User Not Authenticated!"},status=status.HTTP_401_UNAUTHORIZED)

    def put(self,request,isbn):
        token = request.COOKIES.get('jwt_token')
        if token is not None:
            if 'publication_date' not in request.data or 'description' not in request.data:
                return Response({"message":"Incomplete Details"},status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    get_book = Book.objects.get(isbn=isbn)
                    request.data['isbn'] = isbn
                    serializers = BookSerializer(get_book,data=request.data,partial=True)
                    if serializers.is_valid():
                        serializers.save()
                        return Response({"message":"Updated Successfully!","data":serializers.data}, status=status.HTTP_200_OK)
                    else:
                        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                except Book.DoesNotExist:
                    return Response({"message":"Book Not Found!"},status=status.HTTP_404_NOT_FOUND)
        
    
    def delete(self,request,isbn):
        try:
            get_book = Book.objects.get(isbn=isbn)
            serializers = BookSerializer(get_book)
            serializers.delete(get_book)
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)