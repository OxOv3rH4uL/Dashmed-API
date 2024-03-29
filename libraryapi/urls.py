from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('books/', AddBook.as_view(),name='books'),
    path('books/<slug:isbn>/',GetBook.as_view()),
    re_path(r'^.*$', InvalidEndPoint.as_view())
]
