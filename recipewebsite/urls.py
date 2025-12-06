"""urls.py

URL configuration for Recipe Website project.

Routes URLs to views organized by functionality:
- Authentication: user_login, user_register, user_logout
- Browse: index, category, recipe, search_recipes
- User Account: user_account, user_update, user_detail
- Recipe Management: recipe_create, recipe_update, recipe_delete

For more information:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from recipewebsite import views
from django.contrib.auth import views as auth_views

# ============ AUTHENTICATION ============
authentication_patterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]

# ============ BROWSE & DISPLAY ============
browse_patterns = [
    path('', RedirectView.as_view(url='/index/', permanent=False), name='home'),
    path('index/', views.index, name='index'),
    path('category/<int:pk>/', views.category, name='category'),
    path('recipe/<int:pk>/', views.recipe, name='recipe'),
    path('search-recipes/', views.search_recipes, name='search-recipes'),
]

# ============ USER ACCOUNT ============
account_patterns = [
    path('account/', views.user_account, name='account'),
    path('account/edit/', views.user_update, name='edit'),
    path('profile/<int:pk>/', views.user_detail, name='profile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password')
]

# ============ RECIPE MANAGEMENT ============
recipe_patterns = [
    path('recipe/create/', views.recipe_create, name='create_recipe'),
    path('recipe/<int:pk>/edit/', views.recipe_update, name='editRecipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
]

review_patterns = [
    path('review_create/<int:pk>/', views.review_create, name="review_create")
]
# ============ ADMIN ============
admin_patterns = [
    path('admin/', admin.site.urls),
]

# Combine all patterns
urlpatterns = (
    authentication_patterns + 
    browse_patterns + 
    account_patterns + 
    recipe_patterns + 
    admin_patterns +
    review_patterns
)

# Static and media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)