from django.urls import path
from .views import Register as registerView
from .views import Login as loginView
from .views import Home as homeView
from .views import Logout as logoutView

urlpatterns = [
    path('register', registerView.as_view()),
    path('login',loginView.as_view()),
    path('home',homeView.as_view()),
    path('logout',logoutView.as_view())
]
