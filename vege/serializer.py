from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import re
from django.template.defaultfilters import slugify
from core.pagination import LargeResultsSetPagination, StandardResultsSetPagination,CustomPagination
    

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe 
        exclude = [] 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        # fields=['username','id','first_name','last_name']
        fields = ['username']
        

class TodoSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    # user = UserSerializer()  # returns whole object 
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Todo
        exclude = ['created_at'] 
    
    def create(self,validated_data):
        username = validated_data['user']["username"]
        user = User.objects.get(username=username)

        return Todo.objects.create(
            user=user,
            todo_title=validated_data['todo_title'],
            todo_description=validated_data['todo_description']
        )
        

    def get_slug(self,obj):
        return slugify(obj.todo_title)

    def validate_todo_title(self, data):
        if data:
            todo_title = data
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if len(todo_title) < 3:
                raise serializers.ValidationError('todo_tile should not be less than 3 characters')
            if regex.search(todo_title) is not None:
                raise serializers.ValidationError('todo_ title cannot contains special characters')
        return data
