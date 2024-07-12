from django import forms
from django.forms import ModelForm
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

class CreateRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'