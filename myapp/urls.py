from django.urls import path

from myapp import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',  views.home),
    url('recipe/<int:id_recipe>', views.view_recipe, name='view_recipe'),
    url('recipes', views.list_recipes, name='recipes'),
    url('categories', views.list_categories, name='categories'),
]
