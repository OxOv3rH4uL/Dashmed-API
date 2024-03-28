from django.urls import path
from .views import *

urlpatterns = [
    path('books', AddBook.as_view(),name='books'),
    path('books/<slug:isbn>',GetBook.as_view())
]
