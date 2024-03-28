from rest_framework import serializers
from .models import Book,Author
import re
import datetime
from django.core.exceptions import MultipleObjectsReturned

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
    
    def validate_name(self, name):
        if not re.match("^[a-zA-Z .]+$", name):
            raise serializers.ValidationError("Name should contain only letters, spaces, and dots.")
        else:
            return name

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.CharField() 

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author','publication_date','description']  
    
    def validate_isbn(self, isbn):
        if not re.match(r"^(?:\d[\-]?){9}[\d|X]$", isbn) and not re.match(r"^(?:97[89])?\d[\-]?\d{5}[\-]?\d{3}[\-]?\d[\-]?(?:\d|X)$", isbn):
            raise ValueError("Invalid ISBN format.")
        
        return isbn
        

    def validate_publication_date(self, date):
        if date > datetime.date.today():
            raise serializers.ValidationError("Publication Date cannot be in the future.")
        else:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Invalid date format. Date should be in YYYY-MM-DD format.")
        
        return date
        


    def create(self, validated_data):
        author_name = validated_data.pop('author')
        authors = Author.objects.filter(name=author_name)

        if authors.exists():
            author = authors.first()
        else:
            author = Author.objects.create(name=author_name)

        book_data = {
            'author': author,
            'title': validated_data['title'],
            'isbn': validated_data['isbn'],
            'description': validated_data.get('description', ''),
        }

        if 'publication_date' in validated_data:
            book_data['publication_date'] = validated_data['publication_date']

        
        book = Book.objects.create(**book_data)
        return book
    
    def update(self, instance, validated_data):
        author_name = validated_data.pop('author')
        authors = Author.objects.filter(name=author_name)

        if authors.exists():
            author = authors.first()
        else:
            author = Author.objects.create(name=author_name)

        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', author)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.description = validated_data.get('description', instance.description)
        
        
        instance.save()
        return instance
    
    def delete(self,instance):
        instance.delete()
    

        

    