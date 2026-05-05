from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("",login,name="login"),
    path("logout/",logout,name="logout"),
    path('home/',home,name="home"),
    path("register/",register,name="register"),
    path("submit_quiz/<int:id>/",submit_quiz,name="submit_quiz"),
    path("contact_us/",contact_us,name="contact_us"),
    
]
