from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Icons(models.Model):
    icon_name = models.CharField(max_length=255)
    icon_class = models.CharField(max_length=255)
    
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to="recipes",null=True)
    difficulty = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date_updated', '-date_created']

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)
    quantity = models.CharField(max_length=255)

class PreparationStep(models.Model):
    text = models.TextField()
    sequence = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)

    def __str__(self):
        return self.text

class Note(models.Model):
    content = models.TextField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)

    def __str__(self):
        return self.content

class SocialMedia(models.Model):
    icon = models.ForeignKey(Icons, on_delete=models.RESTRICT)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.link
