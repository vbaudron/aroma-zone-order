from myapp.models import AromaUser, Recipe, RecipeBasket, RecipeQuantity, Product, ProductBasket
from django.core.management import BaseCommand



class Command(BaseCommand):
    
    def add_data_to_optimize_basket(self):
        product_1 = 
        
        # add product from recipe to baket
        recipe = Recipe.objects.get_or_create(
            
        )
        user = AromaUser.objects.get(pk=1)
        ProductBasket.add_products_from_recipe(
            user=user,
            recipe=recipe
        )
    
    def handle(self, *arg, **options):
        self.add_data_to_optimize_basket()
        