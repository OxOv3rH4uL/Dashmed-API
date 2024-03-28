from django.urls import path
from .views import Register as registerView
from .views import Login as loginView
from .views import Home as homeView

urlpatterns = [
    path('register', registerView.as_view()),
    path('login',loginView.as_view()),
    path('home',homeView.as_view())
]
