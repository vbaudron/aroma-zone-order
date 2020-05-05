from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from myapp.models import Recipe, Product, Category, ProductBasket, RecipeBasket
from myapp.forms import RecipeToBasketForm

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon App !</h1>
        <p>Facilitateur commande Aroma-Zone</p>
    """)


# ========
# PRODUCTS
# ========

def view_product(request, id_product):
    """
    Vue qui affiche un produit selon son id
    Son ID est le second paramètre de la fonction
    """
    product = Product.objects.get(pk=id_product)
    packagings = product.packagings.all()
    return render(request, 'myapp/product.html', locals())

def list_products(request):
    products = Product.objects.all()
    return render(request, 'myapp/products.html', locals())


# ==========
# CATEGORIES
# ==========

def view_category(request, id_category):
    """
    """
    category = get_object_or_404(Category, id=id_category)
    return render(request, 'myapp/category.html', {"category": category})


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'myapp/categories.html', {"categories": categories})


# ========
# RECIPES
# ========

def view_recipe(request, id_recipe):
    """
    Vue qui affiche une recette selon son identifiant (ou ID, ici un numéro)
    Son ID est le second paramètre de la fonction (pour rappel, le premier
    paramètre est TOUJOURS la requête de l'utilisateur)
    """
    # Get RECIPE
    recipe = Recipe.objects.get(pk=id_recipe)
    products = recipe.ingredients.all()
    
    # Recipe TO Basket
    form = RecipeToBasketForm(request.POST)
    
    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        
    
    return render(request, 'myapp/recipe.html', locals())


def list_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'myapp/recipes.html', locals())


# ===============
# Product BASKETS
# ===============

def view_product_basket(request):
    user_id = 1
    product_basket = ProductBasket.objects.get(user=user_id)
    return render(request, 'myapp/product_basket.html')