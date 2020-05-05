from myapp import views
from django.urls import path


urlpatterns = [
    path(r'^$',  views.home),
    path('recipes', views.list_recipes, name='recipes'),
    path('recipe/<int:id_recipe>', views.view_recipe, name='view_recipe'),
    path('categories', views.list_categories, name='categories'),
    path('products', views.list_products, name='products'),
    path('product/<int:id_product>', views.view_product, name='view_product'),
]
