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
    if request.method == 'POST':
        searched = request.POST['search-recipes']
        recipes = Recipe.objects.filter(name__icontains=searched)
        context = {
            'searched': searched,
            'recipes' : recipes
        }
    return render(request, 'search-recipe.html', context)

def index(request):
    recipes = Recipe.objects.all()
    context = {
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
    recipe = Recipe.objects.get(pk=pk)
    notes = Note.objects.filter(recipe_id=pk)
    steps = PreparationStep.objects.filter(recipe_id=pk).order_by('sequence')
    ingredients = RecipeIngredient.objects.filter(recipe=pk)
    context = {
        "recipe": recipe,
        "notes": notes,
        "steps": steps,
        "ingredients": ingredients
    }
    return render(request, "recipe.html", context)

@login_required(login_url='/login')
def createRecipe(request):
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, request.FILES)
        print("form.creator")
        print(form)
        # form.creator = request.user
        ingredients_formset = IngredientsFormSet(request.POST,  prefix='ingredients')
        steps_formset = PreparationStepFormSet(request.POST, prefix='steps')
        if form.is_valid() and ingredients_formset.is_valid() and steps_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe = form.save()
            ingredients_formset.instance = recipe
            ingredients_formset.save()
            steps_formset.instance = recipe
            steps_formset.save()

            messages.success(request, "Recipe created successfully!")
            return redirect('recipe', pk=recipe.pk)
        else:
            pprint.pprint(form.errors)
            pprint.pprint(form.non_field_errors())
            print("Ingredient errors:", ingredients_formset.errors)
            print("Step errors:", steps_formset.errors)
            messages.error(request, "There's some errors")
    else:
        form = CreateRecipeForm()
        ingredients_formset = IngredientsFormSet(prefix='ingredients')
        steps_formset = PreparationStepFormSet(prefix='steps')
    context = {
        'form': form,
        'ingredients_formset': ingredients_formset,
        'steps_formset': steps_formset
        }
    return render(request, 'edit_recipe.html', context)

@login_required(login_url='/login')
def editRecipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, creator_id=request.user)
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, instance=recipe)
        ingredients_formset = IngredientsFormSet(request.POST, instance=recipe, prefix='ingredients')
        steps_formset = PreparationStepFormSet(request.POST, instance=recipe, prefix='steps')
        for f in ingredients_formset.forms + steps_formset.forms:
            f.empty_permitted = True
        if form.is_valid() and steps_formset.is_valid() and ingredients_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe = form.save()
            ingredients_formset.instance = recipe
            ingredients_formset.save()
            steps_formset.instance = recipe
            steps_formset.save()
            return redirect('recipe', pk=recipe.pk)
        else:
            pprint.pprint(form.errors)
            pprint.pprint(form.non_field_errors())
            print("Ingredient errors:", ingredients_formset.errors)
            print("Step errors:", steps_formset.errors)
    else:
        form = CreateRecipeForm(instance=recipe)
        ingredients_formset = IngredientsFormSet(instance=recipe, prefix='ingredients')
        steps_formset = PreparationStepFormSet(instance=recipe, prefix='steps')
    context = {
        'form': form,
        'ingredients_formset': ingredients_formset,
        'steps_formset': steps_formset
        }
    return render(request, 'edit_recipe.html', context)

@login_required(login_url='/login')
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)

    if recipe.creator != request.user and request.user.is_staff != True:
        messages.error(request, "Num foi oce que criou!")
        return redirect('recipe', pk=pk)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Foi de base")
        return redirect('index')

def loginPage(request):
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
        'page': page
    }
    return render(request, 'login_register.html', context)

def registerUser(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('index')

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
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        socials = SocialMedia.objects.filter(user=request.user.id)
        recipes = Recipe.objects.filter(creator=request.user.id)
    context = {
        'recipes': recipes,
        'user': user,
        'socials': socials
    }
    return render(request, 'account.html', context)

@login_required(login_url='/login')
def editUser(request):
    page = 'edit'
    profile_form = CustomUserChangeForm()
    form = ""
    user = User.objects.get(id=request.user.id)
    context = {
        'form': form,
        'user': user,
        'profile_form': profile_form,
        'page': page
    }
    return render(request, 'edit_user.html', context)

def userProfile(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            return redirect('account')

    user = User.objects.get(pk=pk)
    profile = User.objects.get(pk=pk)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)