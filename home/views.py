from django.shortcuts import render
from django.http import HttpResponse
from core import cache
import json
from .models import Student

# Create your views here.
def home(request, usr="guest"):
    user = usr
    data = "Guest has no data"
    if cache.exists(user):
        data = cache.fetch(user)

    all_user_data ={"user":user,"data":data}

    if request.method == 'POST':
        user = request.POST.get('username_input')
        data = request.POST.get('user_data')
        if user:
            if cache.exists(user):
                data = cache.fetch(user)
                if data is None or data == "":
                    data = "No data was entered for the user"
                cache.insert(user, data)
        else:
            user = "guest"
            data = "Guest has no data"

    # return HttpResponse(json.dumps(data))
    return render(request, "home.html", {'data': data, 'user': user, 'all_user_data': all_user_data})


def users(request):
    return render(request, "index.html")


def about(request):

    st_obj = Student.objects.get()


    context = {'title': 'About'}
    return render(request, "about.html", context)


def server_home(request):
    return render(request,"server_home.html")