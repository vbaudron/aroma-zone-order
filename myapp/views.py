from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from myapp.models import Recipe, Product, Category


def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon App !</h1>
        <p>Facilitateur commande Aroma-Zone</p>
    """)

# ========
# PRODUCTS
# ========

def view_product(request, id):
    """
    Vue qui affiche un produit selon son id
    Son ID est le second paramètre de la fonction
    """
    product = get_object_or_404(Product, id=id)
    return render(request, 'myapp/product.html', {product})

# ==========
# CATEGORIES
# ==========

def view_categorie(request, id_category):
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
    return render(request, 'myapp/recipe.html', locals())


def list_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'myapp/recipes.html', locals())