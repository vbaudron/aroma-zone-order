from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from myapp.models import Category, ContainerFlag, FunctionnalCategoryChoice, MeasurementUnit, Packaging, Product, \
    ProductDetailsFlag, PropertiesFlag, Recipe, RecipeQuantity, MeasurementUnitComparaisonError, UserAroma, \
    ProductBasket

FAKE_URL = "www.google.fr"
DEFAULT_PRICE = 8

# =======
# PRODUCT 
# =======
class ProductTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create Category
        Category.objects.create(
            code=FunctionnalCategoryChoice.ARGILE,
            label="Categorie_1",
            parent=None
        )
        
    def setUp(self):
        self.category = Category.objects.get(pk=1)
        
    def generate_one_product_one_packaging(self):
        
        self.product = Product.objects.create(
            label="product_1",
            category=self.category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )
        
        self.packaging_1 = Packaging.objects.create(
            product=self.product,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )
        
    def generate_one_product_two_packaging(self):
        self.generate_one_product_one_packaging()
        self.packaging_2 = Packaging.objects.create(
            product=self.product,
            quantity=20,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
    # ---------------------
    # get_biggest_packaging
    # ---------------------
    def test_get_biggest_packaging__only_one(self):
        self.generate_one_product_one_packaging()
        
        biggest = self.product.get_biggest_packaging()
        self.assertEqual(biggest, self.packaging_1)
        
    def test_get_biggest_packaging__two(self):
        self.generate_one_product_two_packaging()
        
        biggest = self.product.get_biggest_packaging()
        self.assertEqual(biggest, self.packaging_2)
        
    # ---------------------------------
    # get_smallest_satisfying_packaging
    # ---------------------------------
    def test_get_smallest_satisfying_packaging__no_quantity(self):
        self.generate_one_product_two_packaging()
    
        smallest = self.product.get_smallest_satisfying_packaging()
        self.assertEqual(smallest, self.packaging_1)
            
    def test_get_smallest_satisfying_packaging__small_quantity(self):
        self.generate_one_product_two_packaging()
    
        smallest = self.product.get_smallest_satisfying_packaging(quantity=5)
        self.assertEqual(smallest, self.packaging_1)
            
    def test_get_smallest_satisfying_packaging__medium_quantity(self):
        self.generate_one_product_two_packaging()
    
        smallest = self.product.get_smallest_satisfying_packaging(quantity=15)
        self.assertEqual(smallest, self.packaging_2)
            
    def test_get_smallest_satisfying_packaging__large_quantity(self):
        self.generate_one_product_two_packaging()
    
        smallest = self.product.get_smallest_satisfying_packaging(quantity=25)
        self.assertEqual(smallest, self.packaging_2)
            
    def test_get_smallest_satisfying_packaging__many_packagings(self):
        self.generate_one_product_two_packaging()
    
        packaging_3 = Packaging.objects.create(
            product=self.product,
            quantity=30,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
        packaging_4 = Packaging.objects.create(
            product=self.product,
            quantity=40,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
        # Small Quantity
        smallest = self.product.get_smallest_satisfying_packaging(quantity=5)
        self.assertEqual(smallest, self.packaging_1)
        
    
        # Low Quantity
        smallest = self.product.get_smallest_satisfying_packaging(quantity=15)
        self.assertEqual(smallest, self.packaging_2)
        
        # Medium
        smallest = self.product.get_smallest_satisfying_packaging(quantity=25)
        self.assertEqual(smallest, packaging_3)
            
        # Large
        smallest = self.product.get_smallest_satisfying_packaging(quantity=35)
        self.assertEqual(smallest, packaging_4)
        
        # Too large
        smallest = self.product.get_smallest_satisfying_packaging(quantity=45)
        self.assertEqual(smallest, packaging_4)
        
            
# =========
# PACKAGING 
# =========
class PackagingTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create Category
        Category.objects.create(
            code=FunctionnalCategoryChoice.ARGILE,
            label="Categorie_1",
            parent=None
        )
        
    def setUp(self):
        self.category = Category.objects.get(pk=1)
    
    def generate_one_product_two_packaging(self):
        
        self.product = Product.objects.create(
            label="product_1",
            category=self.category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )
        
        self.packaging_1 = Packaging.objects.create(
            product=self.product,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )
        
        self.packaging_2 = Packaging.objects.create(
            product=self.product,
            quantity=20,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
    # -----------
    # comparaison
    # -----------
    def test_comparaison__gt__(self):
        # SUPERIOR >
        
        # DATA
        self.generate_one_product_two_packaging()
        
        packaging_equals = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_2.quantity,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
        packaging_different_unit = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_2.quantity,
            unit=MeasurementUnit.GRAMS,
            price=DEFAULT_PRICE
        )
        
        # True if nothing
        self.assertTrue(self.packaging_1 > None)
        
        # Basic True
        self.assertTrue(self.packaging_2 > self.packaging_1)
        
        # False if equals
        self.assertFalse(self.packaging_2 > packaging_equals)
        
        # Basic False
        self.assertFalse(self.packaging_1 > self.packaging_2)
        
        # [ERROR]
        with self.assertRaises(MeasurementUnitComparaisonError):
            self.packaging_1 > packaging_different_unit
        
    def test_comparaison__ge__(self):
        # SUPERIOR OR EQUAL >=

        self.generate_one_product_two_packaging()
        
        packaging_equals = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_2.quantity,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        ) 
        
        packaging_different_unit = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_2.quantity,
            unit=MeasurementUnit.GRAMS,
            price=DEFAULT_PRICE
        )
        
        # True if nothing
        self.assertTrue(self.packaging_1 >= None)
        
        # Basic True
        self.assertTrue(self.packaging_2 >= self.packaging_1)
        
        # True if equals
        self.assertTrue(self.packaging_2 >= packaging_equals)
        
        # Basic False
        self.assertFalse(self.packaging_1 >= self.packaging_2)
        
        # [ERROR]
        with self.assertRaises(MeasurementUnitComparaisonError):
            self.packaging_1 >= packaging_different_unit
                
    def test_comparaison__lt__(self):
        # INFERIOR <
        
        # DATA
        self.generate_one_product_two_packaging()
        
        packaging_equals = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_1.quantity,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
        packaging_different_unit = Packaging.objects.create(
            product=self.product,
            quantity=30,
            unit=MeasurementUnit.GRAMS,
            price=DEFAULT_PRICE
        )
        
        # True if nothing
        self.assertTrue(self.packaging_1 < None)
        
        # Basic True
        self.assertTrue(self.packaging_1 < self.packaging_2)
        
        # False if equals
        self.assertFalse(self.packaging_1 < packaging_equals)
        
        # Basic False
        self.assertFalse(self.packaging_2 < self.packaging_1)
        
        # [ERROR]
        with self.assertRaises(MeasurementUnitComparaisonError):
            self.packaging_1 < packaging_different_unit
        
    def test_comparaison__le__(self):
        # SUPERIOR OR EQUAL >=

        self.generate_one_product_two_packaging()
        
        packaging_equals = Packaging.objects.create(
            product=self.product,
            quantity=self.packaging_1.quantity,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        ) 
        
        packaging_different_unit = Packaging.objects.create(
            product=self.product,
            quantity=30,
            unit=MeasurementUnit.GRAMS,
            price=DEFAULT_PRICE
        )
        
        # True if nothing
        self.assertTrue(self.packaging_1 <= None)
        
        # Basic True
        self.assertTrue(self.packaging_1 <= self.packaging_2)
        
        # True if equals
        self.assertTrue(self.packaging_1 <= packaging_equals)
        
        # Basic False
        self.assertFalse(self.packaging_2 <= self.packaging_1)
        
        # [ERROR]
        with self.assertRaises(MeasurementUnitComparaisonError):
            self.packaging_1 <= packaging_different_unit
        
        
# ===============
# RECIPE QUANTITY 
# ===============
 
class RecipeQuantityTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create Category
        category = Category.objects.create(
            code=FunctionnalCategoryChoice.ARGILE,
            label="Categorie_1",
            parent=None
        )
        
        # Create Recipe
        Recipe.objects.create(
            label="recipe_test",
            container_type=ContainerFlag.POT.value,
            conservation=3,
            final_quantity=30,
            final_unit=MeasurementUnit.ML.value,
            level=Recipe.Level.STARTER,
            properties_flag=PropertiesFlag.NONE.value,
            time=10,
            url=FAKE_URL
        )
        
        Product.objects.create(
            label="product_1",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )
        
    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)
        
    # -----------------
    # Packagings Needed
    # -----------------
    def create_packaging_data_for_packaging_needed(self):
       self.packaging_1 = Packaging.objects.create(
            product=self.product,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )
        
       self.packaging_2 = Packaging.objects.create(
            product=self.product,
            quantity=20,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        ) 
        
    def test_packagings_needed__only_one(self):
        self.create_packaging_data_for_packaging_needed()

        # INFERIOR --> Only one packaging needed and shoudl be PACKAGING_1
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=5,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])
        
        # EQUAL --> Only one packaging needed and shoudl be PACKAGING_1
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=self.packaging_1.quantity,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])
        
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=15,
            unit=MeasurementUnit.ML
        )
        
        # SUPERIOR --> Only one packaging needed and shoudl be PACKAGING_2
        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        
    def test_packagings_needed__many(self):
        self.create_packaging_data_for_packaging_needed()

        # 2 Needed : Pack 1 + Pack 2
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=25,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(2, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        self.assertEqual(self.packaging_1, rq.packagings_needed[1])
        
        # 2 Needed : Pack 1 + Pack 2
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=30,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(2, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        self.assertEqual(self.packaging_1, rq.packagings_needed[1])
        
        # 2 Needed : Pack 2 + Pack 2
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=40,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(2, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        self.assertEqual(self.packaging_2, rq.packagings_needed[1])
        
        # RQ
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=59,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(3, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        self.assertEqual(self.packaging_2, rq.packagings_needed[1])
        
        # MANY -- non exact
        packaging_3 = Packaging.objects.create(
            product=self.product,
            quantity=50,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        
        # RQ
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=59,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(2, len(rq.packagings_needed))
        self.assertEqual(packaging_3, rq.packagings_needed[0])
        self.assertEqual(self.packaging_1, rq.packagings_needed[1])

    def test_update_packaging_needed__quantity_change(self):
        self.create_packaging_data_for_packaging_needed()

        # BASE
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=5,
            unit=MeasurementUnit.ML
        )
        
        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])
        
        # new quantity
        new_quantity = 40

        # TODO called
  #      with patch.object(rq, '_RecipeQuantity.__update_packagings_needed') as method_mock:
  #          rq.quantity = new_quantity
  #          method_mock.assert_called_once_with()

        rq.quantity = new_quantity
        self.assertEqual(rq.quantity, new_quantity)
        self.assertEqual(2, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        self.assertEqual(self.packaging_2, rq.packagings_needed[1])

class RecipeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Category
        category = Category.objects.create(
            code=FunctionnalCategoryChoice.ARGILE,
            label="Categorie_1",
            parent=None
        )

        user = User.objects.create_user(
            username="username",
            email="email@test.com",
            password="test"
        )

        UserAroma.objects.create(
            user=user
        )

        # Create Recipe
        Recipe.objects.create(
            label="recipe_test",
            container_type=ContainerFlag.POT.value,
            conservation=3,
            final_quantity=30,
            final_unit=MeasurementUnit.ML.value,
            level=Recipe.Level.STARTER,
            properties_flag=PropertiesFlag.NONE.value,
            time=10,
            url=FAKE_URL
        )

        product = Product.objects.create(
            label="product_1",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        Packaging.objects.create(
            product=product,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)
        self.packaging = Packaging.objects.get(pk=1)
        self.user = UserAroma.objects.get(pk=1)

    def test_add_products_to_basket__one_product_one_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_to_basket(user=self.user)

        # one product one packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 1)
        self.assertEqual(self.packaging, basket[0].packaging)

    def test_add_products_to_basket__one_product_two_packagings(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_to_basket(user=self.user)

        # one product one packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), len(rq.packagings_needed))
        for i in range(len(basket)):
            self.assertEqual(basket[i].packaging, rq.packagings_needed[i])










        