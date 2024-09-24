from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="accounts"),
    path("all/",get_all_accounts,name="accounts")
]