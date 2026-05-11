from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", login, name="login"),
    path("register/", register, name="register"),
    path("home/", home, name="home"),
    path("logout/", logout, name="logout"),
    path("submit_quiz/<int:id>/", submit_quiz, name="submit_quiz"),
    path("contact_us/", contact_us, name="contact_us"),
]
