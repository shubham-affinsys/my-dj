from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from vege.views import *
from rest_framework.authtoken import views
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("home/", include("home.urls")),
    path("polls/", include("polls.urls")),
    path('vege/', include("vege.urls")),
    path('login/', login_page, name="Login"),
    path('logout/', logout_page, name="Logout"),
    path('register/', register_page, name="Register"),

    path('api-token-auth/', views.obtain_auth_token),

    path('logviewer/', include('logviewer.urls')),

    path("", server_home,name='server_home')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()