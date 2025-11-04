from django.contrib import admin
from .models import Category, Ingredient, PreparationStep, Recipe, Note, RecipeIngredient, User, SocialMedia, Icons, Place

class NoteInLine(admin.StackedInline):
    model = Note
    extra = 1

class IngredientInLine(admin.StackedInline):
    model = RecipeIngredient
    extra = 1

class PreparationStepInLine(admin.StackedInline):
    model = PreparationStep
    extra = 1
    
class SocialMediaInLine(admin.StackedInline):
    model = SocialMedia
    extra = 1

class PlaceInline(admin.StackedInline):
    model = Place

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [NoteInLine, IngredientInLine, PreparationStepInLine]
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ["content", "get_recipe"]
    @admin.display(description="Recipe")
    def get_recipe(self, obj):
        return obj.recipe.name
    
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'username', 'is_staff']
    inlines = [SocialMediaInLine]

class PlaceAdmin(admin.ModelAdmin):
    list_display = ["city"]
    model = Place


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Ingredient)
admin.site.register(User, UserAdmin)
admin.site.register(Icons)
admin.site.register(Place, PlaceAdmin)
