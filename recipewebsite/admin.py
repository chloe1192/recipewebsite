"""admin.py

Django admin interface customization for Recipe Website.

Customizes the Django admin interface with inline editors and 
filtered displays for better content management.
"""

from django.contrib import admin
from .models import Category, Ingredient, PreparationStep, Recipe, Note, RecipeIngredient, User, SocialMedia, Icons, Place


# ============ INLINE EDITORS ============

class NoteInLine(admin.StackedInline):
    """Inline editor for recipe notes."""
    model = Note
    extra = 1


class IngredientInLine(admin.StackedInline):
    """Inline editor for recipe ingredients."""
    model = RecipeIngredient
    extra = 1


class PreparationStepInLine(admin.StackedInline):
    """Inline editor for recipe preparation steps."""
    model = PreparationStep
    extra = 1
    

class SocialMediaInLine(admin.StackedInline):
    """Inline editor for user social media profiles."""
    model = SocialMedia
    extra = 1


class PlaceInline(admin.StackedInline):
    """Inline editor for places/cities."""
    model = Place


# ============ ADMIN INTERFACES ============

class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for recipe categories.
    
    Displays:
        name: Category name
    """
    list_display = ["name"]


class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for recipes with inline editors.
    
    Displays:
        name: Recipe name
    
    Inline Editors:
        Notes, Ingredients, Preparation Steps
    """
    list_display = ["name"]
    inlines = [NoteInLine, IngredientInLine, PreparationStepInLine]
    

class NoteAdmin(admin.ModelAdmin):
    """Admin interface for recipe notes.
    
    Displays:
        content: Note content
        get_recipe: Recipe the note belongs to
    """
    list_display = ["content", "get_recipe"]
    
    @admin.display(description="Recipe")
    def get_recipe(self, obj):
        """Display recipe name for each note."""
        return obj.recipe.name
    

class UserAdmin(admin.ModelAdmin):
    """Admin interface for users with inline social media editor.
    
    Displays:
        username: User's username
        email: User's email address
        is_staff: Whether user is staff member
    
    Inline Editors:
        Social Media profiles
    """
    list_display = ['username', 'email', 'is_staff']
    inlines = [SocialMediaInLine]


class PlaceAdmin(admin.ModelAdmin):
    """Admin interface for places/cities.
    
    Displays:
        city: City name
    """
    list_display = ["city"]
    model = Place


# ============ REGISTRATION ============

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Ingredient)
admin.site.register(User, UserAdmin)
admin.site.register(Icons)
admin.site.register(Place, PlaceAdmin)
