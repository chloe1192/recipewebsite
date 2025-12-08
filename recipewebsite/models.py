"""models.py

Database models for Recipe Website application.

Models:
    Place: Geographical location of users
    User: Custom user model extending Django's AbstractUser  
    Category: Recipe categories
    Ingredient: Ingredient reference data
    Icons: Font Awesome icons for recipes
    Recipe: Main recipe model with image processing
    RecipeIngredient: Ingredients for each recipe
    PreparationStep: Steps to prepare a recipe
    Note: User notes on recipes
    SocialMedia: Social media profiles for users
"""

import logging
from PIL import Image
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from location_field.models.plain import PlainLocationField
import re

from recipewebsite import settings

logger = logging.getLogger(__name__)


def resize_and_crop_image(image_path, target_size):
    """Crop and resize images to target dimensions.
    
    Crops image to square then resizes to target size. Used for profile
    avatars (512x512) and recipe images (1920x1080).
    
    Args:
        image_path (str): Path to image file
        target_size (tuple): Target size as (width, height)
    
    Returns:
        None: Image is saved in-place
    
    Logs:
        logger.error: If image processing fails
    """
    try:
        img = Image.open(image_path)
        if img.size != target_size:
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = left + min_dim
            bottom = top + min_dim
            img = img.crop((left, top, right, bottom))
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            img.save(image_path, quality=95)
    except Exception as e:
        logger.error(f"Error resizing image at {image_path}: {str(e)}")

class Place(models.Model):
    """Geographical location/city.
    
    Attributes:
        city (str): City name
        location: Geographic coordinates (PlainLocationField)
    """
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    
    def __str__(self):
        return self.city

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.
    
    Uses email as USERNAME_FIELD for authentication. Extends default User 
    with profile information including bio, avatar, city, and phone.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        username (str): Unique username
        email (str): Unique email address (USERNAME_FIELD)
        bio (str): User biography
        avatar (ImageField): Profile picture auto-resized to 512x512
        city (ForeignKey): Reference to Place model
        phone (str): Phone number
    
    Methods:
        save(): Auto-resizes avatar to 512x512 on save
    """
    first_name = models.CharField(
        max_length=150, 
        null=True, 
        blank=True, 
        default="")
    last_name = models.CharField(max_length=150, blank=True, null=True, default="")
    username = models.CharField(
        max_length=200, 
        null=False, 
        unique=True,
        help_text= 'Escolha um nome de usuario',
        error_messages = {
            'unique': ('Já existe um usuário com esse nome')
        }
    )
    email = models.EmailField(
        unique=True,
        help_text = "Digite seu email",
        error_messages = {
            'unique': ('Já existe um usuário com esse email')
        })
    bio = models.TextField(null=True, default=None, blank=True)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    city = models.ForeignKey(Place, null=True, on_delete=models.RESTRICT, blank=True, default=None)
    phone = models.CharField(max_length=255, null=True, default=None, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def clean(self, *args, **kwargs):
        # Não aceita espaços ou caracteres não permitidos em URLs
        if not re.match(r'^[A-Za-z0-9_-]+$', self.username):
            raise ValidationError({'username': 'O nome de usuário só pode conter letras, números, hífen e underline'})
        return super().clean()
    
    def save(self, *args, **kwargs):
        """Save user and auto-resize avatar to 512x512."""
        super().save(*args, **kwargs)
        if self.avatar:
            resize_and_crop_image(self.avatar.path, (512, 512))

class Category(models.Model):
    """Recipe category/cuisine type.
    
    Attributes:
        name (str): Category name (e.g., 'Italian', 'Mexican', 'Vegan')
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Icons(models.Model):
    """Font Awesome icons for recipes and social media.
    
    Attributes:
        name (str): Icon name
        html_class (str): Font Awesome class (e.g., 'fab fa-instagram')
    """
    name = models.CharField(max_length=255)
    html_class = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    """Main recipe model with approval workflow.
    
    Stores complete recipe information including images, difficulty, duration,
    and approval status. Images are automatically resized on save.
    
    Attributes:
        name (str): Recipe name
        img (ImageField): Recipe main image auto-resized to 1920x1080
        sliderImg (ImageField): Hero slider image auto-resized to 1920x1080
        difficulty (int): Difficulty level 1-5 (1=Very Easy, 5=Very Hard)
        duration (int): Preparation time in minutes (minimum 1)
        description (str): Recipe description/instructions
        category (ForeignKey): Recipe category
        date_created (DateTime): Creation timestamp
        date_updated (DateTime): Last modification timestamp
        creator (ForeignKey): Recipe author (User)
        is_highlight (bool): Featured recipe flag
        is_approved (bool): Admin approval status
    
    Meta:
        ordering: By date_updated then date_created (newest first)
        indexes: For performance optimization on common queries
    
    Methods:
        save(): Auto-resizes images to target dimensions before saving
    """
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to="recipes",null=True,default='default.jpg',)
    sliderImg = models.ImageField(upload_to="recipes",null=True,default='default.jpg',)
    difficulty = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nível de dificuldade de 1 (Muito Fácil) a 5 (Muito Difícil)"
    )
    duration = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Duração em minutos"
    )
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_highlight = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_recipes',
        blank=True
    )

    class Meta:
        # Ordenar por mais recente primeiro
        ordering = ['-date_updated', '-date_created']
        # Índices do banco de dados para consultas comuns
        indexes = [
            models.Index(fields=['-date_updated']),
            models.Index(fields=['creator', 'is_approved']),
        ]
    
    def get_review_average_rating(self):
        avg = Review.objects.filter(recipe=self).aggregate(Avg('rating'))['rating__avg']
        print(self.name , ' rating ', avg)
        return avg or 0
    
    def save(self, *args, **kwargs):
        """Save recipe and auto-resize images to target dimensions."""
        super().save(*args, **kwargs)
        if self.sliderImg:
            resize_and_crop_image(self.sliderImg.path, (1920, 1080))
        if self.img:
            resize_and_crop_image(self.img.path, (1920, 1080))
    
    def delete(self):
        """"Delete recipe and remove associated images from storage."""
        if self.img:
            self.img.delete()
        if self.sliderImg:
            self.sliderImg.delete()
        super().delete()
    
    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    """Ingredients for a recipe with ordering.
    
    Attributes:
        text (str): Ingredient description/measurement
        sequence (int): Order of ingredients (minimum 1)
        recipe (ForeignKey): Parent recipe
    
    Meta:
        ordering: By sequence (1, 2, 3, ...)
    """
    text = models.TextField()
    sequence = models.IntegerField(validators=[MinValueValidator(1)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['sequence']
    
    def __str__(self):
        return self.text


class PreparationStep(models.Model):
    """Step-by-step preparation instructions for a recipe.
    
    Attributes:
        text (str): Step description/instruction
        sequence (int): Order of steps (minimum 1)
        recipe (ForeignKey): Parent recipe
    
    Meta:
        ordering: By sequence (1, 2, 3, ...)
    """
    text = models.TextField()
    sequence = models.IntegerField(validators=[MinValueValidator(1)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.text

class Note(models.Model):
    """User notes/tips for a recipe.
    
    Attributes:
        content (str): Note content
        recipe (ForeignKey): Recipe the note belongs to
    """
    content = models.TextField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class SocialMedia(models.Model):
    """Social media profiles for users.
    
    Attributes:
        social_name (str): Social network name (e.g., 'Instagram', 'Twitter')
        profile_name (str): User's profile name on that network
        icon (ForeignKey): Icon/Font Awesome class from Icons model
        link (str): Direct link to profile
        user (ForeignKey): User who owns the profile
    """
    social_name = models.CharField(max_length=255, null=True)
    profile_name = models.CharField(max_length=255, null=True)
    icon = models.ForeignKey(Icons, on_delete=models.RESTRICT, null=True)
    link = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.link

class Review(models.Model):
    """User reviews and ratings for recipes.
    
    Attributes:
        rating (int): Rating score 1-5
        comment (str): Review comment
        recipe (ForeignKey): Reviewed recipe
        user (ForeignKey): User who wrote the review
    """
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.email} for {self.recipe.name}"