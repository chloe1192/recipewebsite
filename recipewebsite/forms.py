from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Recipe, RecipeIngredient, PreparationStep
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

DIFFICULTY_CHOICES = [
    (1, 'Very Easy'),
    (2, 'Easy'),
    (3, 'Medium'),
    (4, 'Hard'),
    (5, 'Very Hard'),
]

class CreateRecipeForm(ModelForm):

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Recipe
        fields = ['name', 'img', 'sliderImg', 'difficulty', 'duration', 'description', 'category']

# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, PreparationStep


class RecipeIngredientForm(forms.ModelForm):
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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add HTML classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Bootstrap example
                'placeholder': field.label
            })

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'phone']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add HTML classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Bootstrap example
                'placeholder': field.label
            })