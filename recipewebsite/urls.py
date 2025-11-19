"""urls.py

URL configuration for Recipe Website project.

Routes URLs to views organized by functionality:
- Authentication: login, register, logout
- Browse: index, category, recipe, search
- User: account, editUser, profile
- Recipe Management: create_recipe, editRecipe, delete_recipe

For more information:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "recipewebsite"

# ============ AUTHENTICATION ============
authentication_patterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
]

# ============ BROWSE & DISPLAY ============
browse_patterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),
    path('index/', views.index, name='index'),
    path('category/<int:pk>/', views.category, name='category'),
    path('recipe/<int:pk>/', views.recipe, name='recipe'),
    path('search-recipes/', views.search_recipes, name='search-recipes'),
]

# ============ USER ACCOUNT ============
account_patterns = [
    path('account/', views.userAccount, name='account'),
    path('editUser/', views.editUser, name='edit'),
    path('profile/<int:pk>/', views.userProfile, name='profile'),
]

# ============ RECIPE MANAGEMENT ============
recipe_patterns = [
    path('create_recipe/', views.createRecipe, name='create_recipe'),
    path('editRecipe/<int:pk>/', views.editRecipe, name='editRecipe'),
    path('delete_recipe/<int:pk>/', views.delete_recipe, name='delete_recipe'),
]

# ============ ADMIN ============
admin_patterns = [
    path('admin/', admin.site.urls, name='admin'),
]

# Combine all patterns
urlpatterns = authentication_patterns + browse_patterns + account_patterns + recipe_patterns + admin_patterns

# Static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)