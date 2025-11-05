from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from location_field.models.plain import PlainLocationField

class Place(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    
    def __str__(self):
        return self.city

class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=200, null=True, unique="True", default=None)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, default=None, blank=True)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    city = models.ForeignKey(Place, null=True, on_delete=models.RESTRICT, blank=True, default=None)
    phone = models.CharField(max_length=255, null=True, default=None, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',  'password']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        avatar = Image.open(self.avatar.path)
        if avatar.size != (512, 512):
            width, height = avatar.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            avatar = avatar.crop((left, top, right, bottom))
            avatar = avatar.resize((512, 512))
            avatar.save(self.avatar.path)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Icons(models.Model):
    name = models.CharField(max_length=255)
    html_class = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to="recipes",null=True,default='default.jpg',)
    sliderImg = models.ImageField(upload_to="recipes",null=True,default='default.jpg',)
    difficulty = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_highlight = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_updated', '-date_created']
            
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        sliderImg = Image.open(self.sliderImg.path)
        if sliderImg.size != (1920, 1080):
            width, height = sliderImg.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            sliderImg = sliderImg.crop((left, top, right, bottom))
            sliderImg = sliderImg.resize((1920, 1080))
            sliderImg.save(self.sliderImg.path)

        img = Image.open(self.img.path)
        if img.size != (1920, 1080):
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            img = img.crop((left, top, right, bottom))
            img = img.resize((1920, 1080))
            img.save(self.img.path)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    text = models.TextField()
    sequence = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

class PreparationStep(models.Model):
    text = models.TextField()
    sequence = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Note(models.Model):
    content = models.TextField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class SocialMedia(models.Model):
    social_name = models.CharField(max_length=255, null=True)
    profile_name = models.CharField(max_length=255, null=True)
    icon = models.ForeignKey(Icons, on_delete=models.RESTRICT, null=True)
    link = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.link
