from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    publication_date = models.DateField(null=True)
    isbn = models.CharField(max_length = 255, unique = True)    
    description = models.TextField(null=True)

    REQUIRED_FIELDS = ['title','author','isbn']
    
    def __str__(self):
        return self.title
    


    