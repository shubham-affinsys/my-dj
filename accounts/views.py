from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


def index(request):
    return HttpResponse("You are at Accounts")

from django.http import JsonResponse, HttpResponseServerError

def get_all_accounts(request):
        response = requests.get("https://user-svc.vercel.app/users/")
            
        response.raise_for_status()  # Raises an error for 4xx and 5xx responses            
        data = response.json()  # Parse the JSON response

        # Return a JsonResponse for easier handling of JSON in Django
        return JsonResponse(data, safe=False)
