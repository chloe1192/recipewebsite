"""views.py

Request/response handlers for Recipe Website.

Views are organized by functionality:
- Search & Browse: search_recipes, index, category, recipe
- Recipe Management: createRecipe, editRecipe, delete_recipe
- Authentication: loginPage, registerUser, logoutUser
- User Account: userAccount, editUser, userProfile

All views use select_related() for query optimization and pagination
where appropriate. Create/Edit views use @transaction.atomic for 
data consistency.
"""

import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from .forms import CreateRecipeForm, CustomUserChangeForm, CustomUserCreationForm, IngredientsFormSet, PreparationStepFormSet, ReviewForm
from .models import Category, Recipe, Note, PreparationStep, RecipeIngredient, Review, SocialMedia
from .models import User
from django.db.models import Q

logger = logging.getLogger(__name__)

# ============ CONFIGURATION ============
PAGE_SIZE = 12  # Recipes per page


# ============ SEARCH & BROWSE ============

def search_recipes(request):
    """Search recipes by name with pagination.
    
    POST: Search for recipes containing query string
    
    Args:
        request: HTTP request
        search-recipes: Query string from form
    
    Returns:
        Rendered search-recipe.html with paginated results
    """
    context = {}
    if request.method == 'POST':
        searched = request.POST.get('search-recipes', '')
        recipes_list = Recipe.objects.filter(Q(name__icontains=searched) | Q(recipeingredient__text__icontains=searched), is_approved=True).select_related('category', 'creator').distinct()
        paginator = Paginator(recipes_list, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            recipes = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            recipes = paginator.page(1)
        context = {
            'searched': searched,
            'recipes': recipes,
            'paginator': paginator
        }
    return render(request, 'search-recipe.html', context)


def index(request):
    """Display all approved recipes with pagination.
    
    Args:
        request: HTTP request
    
    Returns:
        Rendered index.html with paginated approved recipes
    """
    recipes_list = Recipe.objects.filter(is_approved=True).select_related('category', 'creator')
    paginator = Paginator(recipes_list, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        recipes = paginator.page(1)
    context = {
        "recipes": recipes,
        "paginator": paginator
    }
    for r in recipes:
        r.average_rating = round(r.get_review_average_rating())
        print(r.average_rating)
    return render(request, "index.html", context)


def category(request, pk):
    """Display recipes by category with pagination.
    
    Args:
        request: HTTP request
        pk (int): Category ID
    
    Returns:
        Rendered category.html with recipes in category
    
    Raises:
        Http404: If category does not exist
    """
    category = get_object_or_404(Category, id=pk)
    category_list = Category.objects.all()
    recipes_list = Recipe.objects.filter(category_id=pk, is_approved=True).select_related('category', 'creator')
    paginator = Paginator(recipes_list, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        recipes = paginator.page(1)
    context = {
        "category": category,
        "recipes": recipes,
        "categories": category_list,
        "paginator": paginator
    }
    return render(request, "category.html", context)


def recipe(request, pk):
    """Display single recipe with ingredients, steps, and notes.
    
    Args:
        request: HTTP request
        pk (int): Recipe ID
    
    Returns:
        Rendered recipe.html with complete recipe details
    
    Raises:
        Http404: If recipe does not exist
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    notes = Note.objects.filter(recipe_id=pk).select_related('recipe')
    steps = PreparationStep.objects.filter(recipe_id=pk).order_by('sequence')
    ingredients = RecipeIngredient.objects.filter(recipe=pk)
    review_form = ReviewForm()
    reviews = review_list(request=request, recipe=recipe)
    context = {
        "reviews": reviews,
        "recipe": recipe,
        "notes": notes,
        "steps": steps,
        "ingredients": ingredients,
        "review_form": review_form
    }
    return render(request, "recipe.html", context)


# ============ RECIPE MANAGEMENT ============

@login_required(login_url='/login')
@ratelimit(key='user', rate='20/h', method='POST')
@transaction.atomic
def recipe_create(request):
    """Create new recipe with ingredients and preparation steps.
    
    Rate limited to 20 recipes per hour per user.
    Requires authentication.
    
    GET: Display empty form
    POST: Create recipe if all forms valid
    
    Args:
        request: HTTP request
    
    Returns:
        GET: Rendered edit_recipe.html with empty forms
        POST: Redirect to recipe detail or edit_recipe.html with errors
    """
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, request.FILES)
        ingredients_formset = IngredientsFormSet(request.POST, prefix='ingredients')
        steps_formset = PreparationStepFormSet(request.POST, prefix='steps')
        if form.is_valid() and ingredients_formset.is_valid() and steps_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
            ingredients_formset.instance = recipe
            ingredients_formset.save()
            steps_formset.instance = recipe
            steps_formset.save()
            logger.info(f"Recipe created: {recipe.name} by {request.user.username}")
            messages.success(request, "Recipe created successfully!")
            return redirect('recipe', pk=recipe.pk)
        else:
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Ingredients errors: {ingredients_formset.errors}")
            logger.error(f"Steps errors: {steps_formset.errors}")
            messages.error(request, "There are some errors in the form")
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
@transaction.atomic
def recipe_update(request, pk):
    """Edit existing recipe (creator only).
    
    Requires authentication and recipe ownership.
    
    GET: Display form with recipe data
    POST: Update recipe if all forms valid
    
    Args:
        request: HTTP request
        pk (int): Recipe ID
    
    Returns:
        GET: Rendered edit_recipe.html with populated forms
        POST: Redirect to recipe detail or edit_recipe.html with errors
    
    Raises:
        Http404: If recipe not found or user is not creator
    """
    recipe = get_object_or_404(Recipe, pk=pk, creator=request.user)
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST, instance=recipe)
        ingredients_formset = IngredientsFormSet(request.POST, instance=recipe, prefix='ingredients')
        steps_formset = PreparationStepFormSet(request.POST, instance=recipe, prefix='steps')
        for f in ingredients_formset.forms + steps_formset.forms:
            f.empty_permitted = True
        if form.is_valid() and steps_formset.is_valid() and ingredients_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
            ingredients_formset.instance = recipe
            ingredients_formset.save()
            steps_formset.instance = recipe
            steps_formset.save()
            logger.info(f"Recipe updated: {recipe.name} by {request.user.username}")
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipe', pk=recipe.pk)
        else:
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Ingredients errors: {ingredients_formset.errors}")
            logger.error(f"Steps errors: {steps_formset.errors}")
            for key, value in form.errors.items():
                messages.error(request, value)
            for key, value in ingredients_formset.errors.items():
                messages.error(request, value)
            for key, value in steps_formset.errors.items():
                messages.error(request, value)
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
    """Delete recipe (creator or admin only).
    
    Requires authentication and recipe ownership or staff status.
    Displays confirmation form on GET, deletes on POST.
    
    Args:
        request: HTTP request
        pk (int): Recipe ID
    
    Returns:
        GET: Rendered delete_recipe.html for confirmation
        POST: Redirect to index on success
    
    Raises:
        Http404: If recipe not found
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    # Authorization check: only creator or admin can delete
    if recipe.creator != request.user and not request.user.is_staff:
        messages.error(request, "Você não criou essa receita!")
        return redirect('recipe', pk=pk)
    
    if request.method == 'POST':
        recipe_name = recipe.name
        recipe.delete()
        messages.success(request, f"Receita '{recipe_name}' deletada com sucesso!")
        return redirect('index')
    
    # Render confirmation for GET request
    context = {'recipe': recipe}
    return render(request, 'delete_recipe.html', context)

@login_required(login_url='/login')
def favorite_toggle(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.favorited_by.all():
        recipe.favorited_by.remove(request.user)
    else:
        recipe.favorited_by.add(request.user)
    return redirect('recipe', pk=pk)

# ============ AUTHENTICATION ============

def user_login(request):
    """User login view.
    
    Redirects authenticated users to index.
    
    GET: Display login form
    POST: Authenticate user with email/username and password
    
    Args:
        request: HTTP request
        username: Email or username
        password: User password
    
    Returns:
        GET: Rendered login_register.html
        POST: Redirect to index on success or redisplay with errors
    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não existe')
            user = None

        if user is not None:
            auth = authenticate(request, email=email, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.error(request, 'Senha incorreta')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def user_register(request):
    """User registration view.
    
    Redirects authenticated users to index.
    
    GET: Display registration form
    POST: Create new user if form valid
    
    Args:
        request: HTTP request
    
    Returns:
        GET: Rendered login_register.html with form
        POST: Redirect to index on success or redisplay with errors
    """
    page = 'register'
    if request.user.is_authenticated:
        return redirect('index')

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
            for key, value in form.errors.items():
                messages.error(request, value)
    context = {
        'form': form,
        'page': page
    }
    return render(request, 'login_register.html', context)


def user_logout(request):
    """User logout view.
    
    Args:
        request: HTTP request
    
    Returns:
        Redirect to index
    """
    logout(request)
    return redirect('index')

def reset_password(request):
    pass

@login_required(login_url='/login')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if request.user == user or request.user.is_staff:
            user.delete()
            messages.success(request, "Usuário deletado com sucesso!")
            return redirect('index')
        if request.user != user and not request.user.is_staff:
            messages.error(request, "Você não pode deletar esse usuário!")
            return redirect('profile', pk=pk)
    else:
        context = {'user': user}
        return render(request, 'user_delete.html', context)
    
    

# ============ USER ACCOUNT ============

@login_required(login_url='/login')
def user_account(request):
    user = request.user
    socials = SocialMedia.objects.filter(user=user)
    recipes = Recipe.objects.filter(creator=user)
    context = {
        'recipes': recipes,
        'user': user,
        'socials': socials
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    """Edit current user's profile information.
    
    Requires authentication.
    
    GET: Display form with user data
    POST: Update user profile if form valid
    
    Args:
        request: HTTP request
    
    Returns:
        GET: Rendered edit_user.html with form
        POST: Redirect to account on success or redisplay with errors
    """
    page = 'edit'
    user = request.user
    profile_form = CustomUserChangeForm(instance=user)
    
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            logger.info(f"User profile updated: {user.username}")
            messages.success(request, "Profile updated successfully!")
            return redirect('account')
        else:
            for key, value in profile_form.errors.items():
                messages.error(request, value)
    
    context = {
        'profile_form': profile_form,
        'user': user,
        'page': page
    }
    return render(request, 'edit_user.html', context)


def user_detail(request, pk):
    """Display user's public profile.
    
    Redirects to account page if viewing own profile.
    
    Args:
        request: HTTP request
        pk (int): User ID
    
    Returns:
        Rendered profile.html with user information
    
    Raises:
        Http404: If user not found
    """

    user = get_object_or_404(User, pk=pk)
    print(user.last_name)
    context = {}
    recipes = Recipe.objects.filter(creator=user, is_approved=True)
    print(recipes.count)
    socials = SocialMedia.objects.filter(user=user)
    context = {
        'user': user,
        'recipes': recipes,
        'socials': socials
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/account')
        else:
            for k, v in form.error_messages.items():
                if not k == 'password_mismatch':
                    messages.error(request, v)
            
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {form: 'form'})
    

# ============ REVIEWS ============

@login_required(login_url='/login')
def review_create(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user == recipe.creator:
            messages.error(request, 'Voce nao pode avaliar sua propria receita')
            return redirect('/recipe/' + str(recipe.id))
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.save()
            messages.success(request, 'Avaliacao publicada com sucesso')
            return redirect('/recipe/' + str(recipe.id))
        else:
            messages.error(request, form.errors)
            return redirect('/recipe/' + str(recipe.id))
    else:
        return redirect('/recipe/' + str(recipe.id))

@login_required(login_url='/login')
def review_update(request, pk):
    instance = get_object_or_404(Review, pk=pk)    
    form = ReviewForm(instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save
            return redirect('recipe', pk=instance.recipe)
    else:
        return redirect('recipe', pk=instance)

def review_list(request, recipe):
    reviews = Review.objects.filter(recipe=recipe)
    
    return reviews

@login_required(login_url='/login')
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    recipe = review.recipe
    review.delete()
    return redirect('recipe', pk=recipe.id)