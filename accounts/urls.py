from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="accounts"),
    path("all",get_all_accounst,name="accounts")
]