from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests

# Create your views here.

def index(request):
    return HttpResponse("You are at Accounts")

from django.http import JsonResponse, HttpResponseServerError

def get_all_accounts(request):
    try:
        response = requests.get("https://user-svc.vercel.app/users/")
        
        # Check if the request was successful
        response.raise_for_status()  # Raises an error for 4xx and 5xx responses
        
        data = response.json()  # Parse the JSON response
        
        # Return a JsonResponse for easier handling of JSON in Django
        return JsonResponse(data, safe=False)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return HttpResponseServerError("Failed to retrieve data from users service.")
    
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
        return HttpResponseServerError("An error occurred while trying to connect to users service.")
    
    except ValueError:
        return HttpResponseServerError("Invalid JSON response from users service.")

