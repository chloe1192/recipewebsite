import pprint
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateRecipeForm, CustomUserChangeForm, CustomUserCreationForm, IngredientsFormSet, PreparationStepFormSet
from .models import Category, Recipe, Note, PreparationStep, Ingredient, RecipeIngredient, SocialMedia
from .models import User

def search_recipes(request):
    category_list = Category.objects.all()
    if request.method == 'POST':
        searched = request.POST['search-recipes']
        recipes = Recipe.objects.filter(name__icontains=searched)
        context = {
            "categories":category_list,
            'searched': searched,
            'recipes' : recipes
        }
    return render(request, 'search-recipe.html', context)

def index(request):
    category_list = Category.objects.all()
    recipes = Recipe.objects.all()
    context = {
            "categories":category_list,
            "recipes":recipes
        }
    return render(request, "index.html", context)

def category(request, pk):
    category_list = Category.objects.all()
    for object in category_list:
        if object.id == pk:
            category = object
            recipes = Recipe.objects.filter(category_id=pk)
    context = {
        "category":category,
        "recipes":recipes,
        "categories":category_list
    }
    return render(request, "category.html", context)

def recipe(request, pk):
    category_list = Category.objects.all()
    recipe = Recipe.objects.get(pk=pk)
    notes = Note.objects.filter(recipe_id=pk)
    steps = PreparationStep.objects.filter(recipe_id=pk).order_by('sequence')
    ingredients = RecipeIngredient.objects.filter(recipe=pk)
    context = {
        "categories": category_list,
        "recipe": recipe,
        "notes": notes,
        "steps": steps,
        "ingredients": ingredients
    }
    return render(request, "recipe.html", context)

@login_required(login_url='/login')
def createRecipe(request):
    category_list = Category.objects.all()
    form = CreateRecipeForm()
    formset = IngredientsFormSet(request.POST)
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.instance = recipe
            formset.save()
            return redirect('index', pk=recipe.pk)
    else:
        form = CreateRecipeForm()
        formset = IngredientsFormSet()
    context = {
        "categories": category_list,
        'form': form,
        'formset': formset
        }
    return render(request, 'create_recipe.html', context)

def editRecipe(request, pk):
    category_list = Category.objects.all()
    recipe = get_object_or_404(Recipe, pk=pk, creator_id=request.user)
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, instance=recipe)
        ingredientsformset = IngredientsFormSet(request.POST, instance=recipe, prefix='ingredients')
        stepformset = PreparationStepFormSet(request.POST, instance=recipe, prefix='steps')
        if form.is_valid() and stepformset.is_valid() and ingredientsformset.is_valid():
            form.save()
            ingredientsformset.instance = recipe
            ingredientsformset.save()
            stepformset.instance = recipe
            stepformset.save()
            return redirect('recipe', pk=recipe.pk)
        else:            
            pprint.pprint(form.errors)
            pprint.pprint(form.non_field_errors())
            print("Ingredient errors:", ingredientsformset.errors)
            print("Step errors:", stepformset.errors)
    else:
        form = CreateRecipeForm(instance=recipe)
        ingredientsformset = IngredientsFormSet(instance=recipe, prefix='ingredients')
        stepformset = PreparationStepFormSet(instance=recipe, prefix='steps')
    context = {
        "categories": category_list,
        'form': form,
        'ingredientsformset': ingredientsformset,
        'stepformset': stepformset
        }
    return render(request, 'edit_recipe.html', context)

def loginPage(request):
    category_list = Category.objects.all()
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'User or pass does not match')

    context = {
        "categories": category_list,
        'page': page
    }
    return render(request, 'login_register.html', context)

def registerUser(request):
    category_list = Category.objects.all()
    page = 'register'
    profile_form = CustomUserCreationForm()
    form = ""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            form = CustomUserCreationForm()
            messages.error(request, 'An error occured, check all fields')
    context = {
        "categories": category_list,
        'form': form,
        'profile_form': profile_form,
        'page': page
    }
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login')
def userAccount(request):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        socials = SocialMedia.objects.filter(user=request.user.id)
    context = {
        "categories": category_list,
        'user': user,
        'socials': socials
    }
    return render(request, 'account.html', context)
    
def editUser(request):    
    category_list = Category.objects.all()
    page = 'edit'
    profile_form = CustomUserChangeForm()
    form = ""
    user = User.objects.get(id=request.user.id)
    context = {
        "categories": category_list,
        'form': form,
        'user': user,
        'profile_form': profile_form,
        'page': page
    }
    return render(request, 'edit_user.html', context)

def userProfile(request, pk):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        if request.user.id == pk:
            return redirect('account')

    user = User.objects.get(pk=pk)
    profile = User.objects.get(pk=pk)
    context = {
        'categories': category_list,
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)