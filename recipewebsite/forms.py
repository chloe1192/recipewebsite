from django import forms
from django.forms import ModelForm
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CreateRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        model = get_user_model()
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))