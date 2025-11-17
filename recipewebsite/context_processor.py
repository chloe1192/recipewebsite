"""context_processor.py

Django context processors for Recipe Website.

Context processors add variables to all template contexts.
"""

from .models import Category


def categories_processor(request):
    """Add all categories to template context.
    
    Makes all recipe categories available to all templates
    via the 'all_categories' variable.
    
    Args:
        request: HTTP request
    
    Returns:
        dict: Context dictionary with 'all_categories' key
    """
    categories = Category.objects.all()
    return {
        'all_categories': categories
    }