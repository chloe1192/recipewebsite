"""
URL configuration for recipewebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "recipewebsite"
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    # front
    path("", views.index, name="index"),
    path("<int:pk>/category", views.category, name="category"),
    path("<int:pk>/recipe/", views.recipe, name="recipe"),
    path('create_recipe/', views.createRecipe),
    path('profile/<int:pk>', views.userProfile, name='profile'),
    #user
    path('account/', views.userAccount, name='account'),
    #admin panel
    path('admin/', admin.site.urls, name='create_recipe'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)