from .views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todo-view-set',TodoViewSet,basename='todo')

urlpatterns = [
    path("recipes/", recipes, name="Recipes"),
    path('delete-recipe/<id>/', delete_recipe, name="delete recipe"),
    path('update-recipe/<id>/', update_recipe, name="delete recipe"),
    path("post_recipes/" ,post_recipes,name="post_recipes"),

    # fn based api view
    path('about/',about,name="vege About"),
    path('post-todo/',post_todo,name='Post Todo'),
    path('get-todo/',get_todo,name='get Todo'),
    path('patch-todo/', patch_todo, name='patch Todo'),

    # class based api view
    path('todo/',TodoView.as_view(),name="Todo"),

    path('api-auth/', include('rest_framework.urls'))
]

# viewset  --> to register need to use router
urlpatterns += router.urls