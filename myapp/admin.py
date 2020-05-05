from django.contrib import admin
from myapp.models import Product, Category, Recipe, RecipeQuantity, Packaging, UserAroma, ProductBasket, RecipeBasket, UserStock

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(RecipeQuantity)
admin.site.register(Packaging)
admin.site.register(UserAroma)
admin.site.register(ProductBasket)
admin.site.register(RecipeBasket)