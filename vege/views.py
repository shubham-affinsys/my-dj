from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from django.core.paginator import Paginator

from core.redis_pub import pub
from core import rabbitmq
from core.redis_pub import my_debugger

# from .helper import paginate
from core.pagination import CustomPagination,StandardResultsSetPagination
# Create your views here.

from django.core.cache import cache
from django.http import HttpResponse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from django.http import JsonResponse

from core import cache

@login_required(login_url="/login/")
def post_recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        recipe = Recipe.objects.create(
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description
        )
        logger.info("recipe stored successfully =====>", recipe.id)
        return redirect("/vege/recipes/")
    
    queryset=None
    # queryset = cache.get('all_recipes')
    if not queryset:
        queryset = Recipe.objects.all().order_by('-recipe_view_count')  # - for sorting in desc
        # cache.set('all-recipes',queryset,timeout=60*60)
        logger.info("Todo added to cache with timeout")

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    # rabbitmq.publish_message(request.user,f"{request.user.username} --- request:GET --- data:all_recipes")
    logger.info("All recipies fethed for user success")
    context = {'recipes': queryset}
    return render(request, 'recipes.html', context=context)



def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    logger.info(f"recipe deleted ===>{id}")
    return redirect('/vege/recipes/')


def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    if request.method != "POST":
        context = {'recipe': queryset}
        return render(request, 'update_recipe.html', context)
    data = request.POST
    recipe_image = request.FILES.get('recipe_image')
    queryset.recipe_name = data.get('recipe_name')
    queryset.recipe_description = data.get('recipe_description')

    if recipe_image:
        queryset.recipe_image = recipe_image

    # Recipe.objects.filter(id=id).update(
    #     recipe_image=recipe_image,
    #     recipe_name=recipe_name,
    #     recipe_description=recipe_description
    # )

    queryset.save()
    logger.info(f"recipe updated successfully =====>{id}")
    return redirect("vege/recipes/")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages(request, 'user not found')
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)
        if user is None or user == '':
            messages(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)  # this method of django maintains session of user login
            logger.info(f"{user}-->logged in")
            return redirect('/vege/recipes/')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    logger.info("User logged out")
    cache.clear()
    return redirect('/login/')


def register_page(request):
    if request.method != 'POST':
        return render(request, 'register.html')
    data = request.POST
    first_name = data.get("first_name")
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    email = f"{first_name}.{last_name}@gmail.com"
    # check if the username already exists
    user = User.objects.filter(username=username)
    if user.exists():
        messages.error(request, 'Username already taken')
        return redirect('/register/')
    
    user = User.objects.create(first_name=first_name, last_name=last_name, username=username,email=email)
    user.set_password(password)
    user.save()
    messages.success(request, 'Account created successfully')
    logger.info('Account created successfully')
    return redirect('/register/')

    


#####
"""
serializing using function based api view
-not manageable
-need to create multiple functions
-we will use class based api view
"""


# decorator that modifies the existing function as an api
# need to allow methods otherwise only get is allowed as  default
@api_view(['GET', 'POST', 'PATCH'])
def about(request):
    if request.method == 'GET':
        return Response({
            'status': 200,
            'message': 'Django rest framework is working',
            'method_called': 'You called GET method'
        })

    elif request.method == 'POST':
        return Response({
            'status': 200,
            'message': 'Django rest framework is working',
            'method_called': 'You called POST method'
        })

    elif request.method == 'PATCH':
        return Response({
            'status': 200,
            'message': 'Django rest framework is working',
            'method_called': 'You called PATCH method'
        })
    else:
        return Response({
            'status': 400,
            'message': 'Django rest framework is working',
            'method_called': 'method not present'
        })


# serialise data during saving
@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializer(data=data)

        # only checks if all fields are entered
        # use validate fn inside serializer to check if the field data is valid
        # like todo_title should not contain any special characters
        if serializer.is_valid():
            serializer.save()  # auto save the data if valid
            print(serializer.data)
            return Response({
                'status': True,
                'message': 'Success data',
                'data': serializer.data
            })

        return Response({
            'status': False,
            'message': 'Invalid data',
            'data': serializer.error
        })

    except Exception as e:
        print(e)
    return Response({
        'status': False,
        'message': 'Something went wrong',
    })


# deserilaize data when accessing
@api_view(['GET'])
def get_todo(request):
    todo_objs = Todo.objects.all()
    serializer = TodoSerializer(todo_objs, many=True)

    try:
        cache.set('todo_all',serializer.data,timeout=60*60)
        logger.info("Todo added to cache with timeout")
    except Exception as e:
        logger.error(f"Cannot connect to redis :{e}")

    return Response({
        "status": True,
        "message": "Todos fethced",
        "data": serializer.data
    })


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                'status': False,
                'message': 'uid is needed',
                'data': {}
            })
        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'updated data successfully',
                'data': serializer.data
            })
        return Response({
            'status': False,
            'message': 'invalid data',
            'data': serializer.error
        })


    except Exception as e:
        print(e)

    return Response({
        'status': False,
        'message': 'Something went wrong, Invalid UID',
    })


"""
class based api view
-cannot add other custom functions
"""
from rest_framework.authtoken.models import Token
from core import cache as cc


class TodoView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = None

        # Try fetching serialized data from cache
        try:
            data = cache.fetch(f"todos_serialized_user_6{request.user.id}")
            if data:
                logger.info("Fetched serialized data from cache.")
        except Exception as e:
            logger.error(f"Error while fetching serialized data from cache: {e}")

        # If not in cache, fetch from the database
        if not data:
            todo_objs = Todo.objects.filter(user=request.user.id)
            logger.info("Fetched queryset from database.")

            serializer = TodoSerializer(todo_objs, many=True)
            data = serializer.data

            try:
                cache.insert(f"todos_serialized_user_6{request.user.id}",data, 30)  # Cache for 10 minutes
                logger.info("Cached the serialized data.")
            except Exception as e:
                logger.error(f"Error occurred while caching serialized data: {e}")

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(data, request)
        
        # Return paginated response
        response = {
            "links": {
                "next": None,
                "previous": None
            },
            "count": 4,
            "results":data
        }
        # return Response(response)
        return paginator.get_paginated_response(paginated_queryset)


    

    def post(self, request):
        try:
            data = request.data
            logger.info(data)
            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                rabbitmq.publish_message(request.user,f"{request.user.username} added uid: {serializer.data['uid']}Todo has been saved")
                logger.info("Succcesfully created todo")
                return Response({
                    'status': True,
                    'message': 'Successfully created todo',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            logger.warning("Todo creation failed invalid data entered")
            return Response({
                'status': False,
                'message': 'Invalid data',
                'data':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"error occured while creating todo : {e}")
            return Response({
                'status': False,
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            if not data.get('uid'):
                return Response({
                    'status': False,
                    'message': 'uid is needed',
                    'data': {}
                })
            obj = Todo.objects.get(uid=data.get('uid'))
            serializer = TodoSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info("Todo updated success")
                return Response({
                    'status': True,
                    'message': 'updated todo'
                })
            logger.error("Todo updation failed invalid data entered")
            return Response({
                'status': False,
                'message': 'invalid data',
                'data':serializer.errors
            })

        except Exception as e:
            logger.error(f"error occured while updating todo : {e}")
            return Response({
                'status': False,
                'message': 'Something went wrong',
            })

    def delete(self,request):
        try:
            data = request.data
            if not data.get('uid'):
                logger.info(f"{request.user} not provided uid")
                return Response({
                    'status': False,
                    'message': 'uid is needed',
                })
            obj = Todo.objects.filter(uid=data.get('uid')).delete()
            if obj[0]==0:
                logger.info("todo not found")
                return Response({
                    'status':False,
                    "message":"todo does not exist"
                })
            else:
                logger.info(f"{request.user} deleted a todo (uid:{data.get('uid')})")
                return Response({
                    'status': True,
                    'message': 'todo deleted successfully',
                })
        except Exception as e:
            logger.error(f"error while deleting=====>{e}")
            return Response({
                'status': False,
                'message': 'Something went wrong',
            })


    """
Model viewset
+ auto handles without creating http methods --> get post patch put delete
+ only 2 line of code
"""

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

##############################


# connectin gwith react myrct
@api_view(['GET'])
def recipes(request):

    recipe = cache.fetch('all-recipes')
    if recipe:
        logger.info("recipes fetched from cache")
        return Response(recipe)
    
    queryset = Recipe.objects.all().order_by('-recipe_view_count')
    logger.info("DB accssed to fetch recipes")
    serializer = RecipeSerializer(queryset,many=True)

    try:
        cache.insert('all-recipes',serializer.data,ex=30)
        logger.info("Todo added to cache with timeout 10")
    except Exception as e:
        logger.error(f"Cannot connect to redis :{e}")
    
    return Response(serializer.data)