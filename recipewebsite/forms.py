"""forms.py

Django form definitions for Recipe Website.

Forms handle validation and rendering for:
- Recipe creation and editing
- Recipe ingredients and preparation steps
- User registration and profile editing
"""

from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Recipe, RecipeIngredient, PreparationStep, Review
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# ============ CONSTANTS ============

DIFFICULTY_CHOICES = [
    (1, 'Very Easy'),
    (2, 'Easy'),
    (3, 'Medium'),
    (4, 'Hard'),
    (5, 'Very Hard'),
]


# ============ RECIPE FORMS ============

class CreateRecipeForm(ModelForm):
    """Recipe creation and editing form.
    
    Includes validation for image file sizes and recipe details.
    
    Attributes:
        MAX_UPLOAD_SIZE: Maximum image file size (5MB)
        difficulty: RadioSelect widget for difficulty 1-5
    
    Validation:
        clean_img(): Validates main image size
        clean_sliderImg(): Validates slider image size
    """
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Recipe
        fields = ['name', 'img', 'sliderImg', 'difficulty', 'duration', 'description', 'category']

    def clean_img(self):
        """Validate main image file size."""
        img = self.cleaned_data.get('img')
        if img and img.size > self.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(f"Image size must be less than 5MB. Current: {img.size / 1024 / 1024:.2f}MB")
        return img

    def clean_sliderImg(self):
        """Validate slider image file size."""
        img = self.cleaned_data.get('sliderImg')
        if img and img.size > self.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(f"Image size must be less than 5MB. Current: {img.size / 1024 / 1024:.2f}MB")
        return img


class RecipeIngredientForm(forms.ModelForm):
    """Form for individual recipe ingredients.
    
    Used in IngredientsFormSet for managing ingredients.
    
    Attributes:
        text: Textarea field for ingredient description
        sequence: NumberInput for ingredient order
    """
    class Meta:
        model = RecipeIngredient
        fields = "__all__"
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter ingredient',
                'required': 'required',
            }),
            'sequence': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PreparationStepForm(forms.ModelForm):
    """Form for individual preparation steps.
    
    Used in PreparationStepFormSet for managing steps.
    
    Attributes:
        text: Textarea field for step description
        sequence: NumberInput for step order
    """
    class Meta:
        model = PreparationStep
        fields = "__all__"
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter preparation step',
                'required': 'required',
            }),
            'sequence': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ============ FORMSETS ============

IngredientsFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)

PreparationStepFormSet = inlineformset_factory(
    Recipe,
    PreparationStep,
    form=PreparationStepForm,
    extra=1,
    can_delete=True
)


# ============ AUTHENTICATION FORMS ============

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form.
    
    Extends Django's UserCreationForm with email, first_name, and last_name.
    All fields automatically get Bootstrap styling.
    
    Fields:
        email (EmailField): User email address
        username (CharField): Unique username
        first_name (CharField): User's first name
        last_name (CharField): User's last name
        password1 (CharField): Password
        password2 (CharField): Password confirmation
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Initialize form and add Bootstrap classes to all fields."""
        super().__init__(*args, **kwargs)
        # Add HTML classes to all fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class CustomUserChangeForm(UserChangeForm):
    """Custom user profile editing form.
    
    Allows users to edit profile information including bio and phone.
    All fields automatically get Bootstrap styling.
    
    Fields:
        email (EmailField): User email
        username (CharField): Unique username
        first_name (CharField): User's first name
        last_name (CharField): User's last name
        bio (TextField): User biography
        phone (CharField): Contact phone number
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'phone']
        
    def __init__(self, *args, **kwargs):
        """Initialize form and add Bootstrap classes to all fields."""
        super().__init__(*args, **kwargs)
        # Add HTML classes to all fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        