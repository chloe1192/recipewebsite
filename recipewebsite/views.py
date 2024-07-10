from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateRecipeForm, CustomUserCreationForm
from .models import Category, ProfileUser, Recipe, Note, PreparationStep, Ingredient, RecipeIngredient
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        "categories": category_list,
        'form': form
        }
    return render(request, 'create_recipe.html', context)

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
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occured, check all fields')
    context = {
        "categories": category_list,
        'form': form,
        'page': page
    }
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login')
def myUserProfile(request):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
    context = {
        "categories": category_list,
        'user': user
    }
    return render(request, 'my_profile.html', context)
    
def userProfile(request, pk):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        if request.user.id == pk:
            return redirect('my_profile_page')

    user = User.objects.get(pk=pk)
    profile = ProfileUser.objects.get(pk=pk)
    context = {
        'categories': category_list,
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)