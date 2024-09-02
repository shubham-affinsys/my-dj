from django.urls import path
from .views import *
# from . import views
# then views.index

urlpatterns = [
    path("", home, name="home"),
    path("users/", users, name="users"),
    path("about/",about, name="about"),
    path("users/<str:usr>/", users, name="user"),
]
