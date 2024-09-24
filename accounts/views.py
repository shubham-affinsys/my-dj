from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def index(request):
    return HttpResponse("You are at Accounts")

def get_all_accounst(request):
    response  = requests.get("https://user-svc.vercel.app/users/")
    data = response.json()
    return HttpResponse(data,content_type="application/json")
