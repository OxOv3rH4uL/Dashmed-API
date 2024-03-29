from django.urls import path,re_path
from .views import Register as registerView
from .views import Login as loginView
from .views import Home as homeView
from .views import Logout as logoutView
from .views import InvalidEndPoint

urlpatterns = [
    path('register', registerView.as_view()),
    path('login',loginView.as_view()),
    path('home',homeView.as_view()),
    path('logout',logoutView.as_view()),
    re_path(r'^.*$', InvalidEndPoint.as_view())
]
