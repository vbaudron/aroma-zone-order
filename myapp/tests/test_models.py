from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from myapp.models import Category, ContainerFlag, FunctionnalCategoryChoice, MeasurementUnit, Packaging, Product, \
    ProductDetailsFlag, PropertiesFlag, Recipe, RecipeQuantity, MeasurementUnitComparaisonError, AromaUser, \
    ProductBasket, RecipeBasket

FAKE_URL = "www.google.fr"
DEFAULT_PRICE = Decimal("8.00")


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


# ======
# RECIPE
# ======
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

        AromaUser.objects.create(
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

        product_1 = Product.objects.create(
            label="product_1",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        product_2 = Product.objects.create(
            label="product_2",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        Packaging.objects.create(
            product=product_1,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

        Packaging.objects.create(
            product=product_2,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)
        self.product_1 = Product.objects.get(pk=1)
        self.product_2 = Product.objects.get(pk=2)
        self.packaging_1 = Packaging.objects.get(pk=1)
        self.packaging_2 = Packaging.objects.get(pk=2)
        self.user = AromaUser.objects.get(pk=1)

    # ------------------------
    # get_all_packaging_needed
    # ------------------------
    def test_get_all_packaging_needed__one_product_one_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        packaging_result = self.recipe.get_all_packaging_needed()
        self.assertEqual(len(packaging_result), 1)
        self.assertEqual(self.packaging_1, packaging_result[0])

    def test_get_all_packaging_needed__one_product_two_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        packaging_result = self.recipe.get_all_packaging_needed()

        # one product two packaging
        self.assertEqual(len(packaging_result), len(rq.packagings_needed))
        for i in range(len(packaging_result)):
            self.assertEqual(packaging_result[i], rq.packagings_needed[i])

    def test_get_all_packaging_needed__two_products_one_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        rq_2 = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_2,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        packaging_result = self.recipe.get_all_packaging_needed()
        self.assertEqual(len(packaging_result), 2)
        self.assertEqual(self.packaging_1, packaging_result[0])
        self.assertEqual(self.packaging_2, packaging_result[1])

    def test_get_all_packaging_needed__two_products_two_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        rq_2 = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_2,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        packaging_result = self.recipe.get_all_packaging_needed()
        self.assertEqual(len(packaging_result), 4)
        self.assertEqual(self.packaging_1, packaging_result[0])
        self.assertEqual(self.packaging_1, packaging_result[1])
        self.assertEqual(self.packaging_2, packaging_result[2])
        self.assertEqual(self.packaging_2, packaging_result[3])

    def test_get_all_packaging_needed__one_product_two_recipes_quantity(self):
        self.product_1.drop_to_ml = Decimal('0.05')
        self.product_1.drop_to_ml = Decimal('0.05')

      #  self.product_1.save()

        rq_drop = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.GOUTTE
        )


        rq_gram = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.GRAMS
        )

        rq_ml = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        # Not all added

        #



        packaging_result = self.recipe.get_all_packaging_needed()


    # ---------------------
    # add_product_to_basket
    # ---------------------
    def test_add_products_to_basket__one_product_one_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_ingredients_to_basket(user=self.user)

        # one product one packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 1)
        self.assertEqual(self.packaging_1, basket[0].packaging)

    def test_add_products_to_basket__one_product_two_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_ingredients_to_basket(user=self.user)

        # one product two packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), len(rq.packagings_needed))
        for i in range(len(basket)):
            self.assertEqual(basket[i].packaging, rq.packagings_needed[i])

    def test_add_products_to_basket__two_products_one_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        rq_2 = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_2,
            _quantity=5,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_ingredients_to_basket(user=self.user)

        # one product one packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 2)
        self.assertEqual(self.packaging_1, basket[0].packaging)
        self.assertEqual(self.packaging_2, basket[1].packaging)

    def test_add_products_to_basket__two_products_two_packaging(self):
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_1,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        rq_2 = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product_2,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        # nothing in basket at first
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        # Add recipe to basket
        self.recipe.add_ingredients_to_basket(user=self.user)

        # one product one packaging
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 4)
        self.assertEqual(self.packaging_1, basket[0].packaging)
        self.assertEqual(self.packaging_1, basket[1].packaging)
        self.assertEqual(self.packaging_2, basket[2].packaging)
        self.assertEqual(self.packaging_2, basket[3].packaging)


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
            url=FAKE_URL,
            density=Decimal('1.50'),
            ml_to_goutte=Decimal('0.05')
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
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

    def test_packaging_needed__only_one(self):

        self.create_packaging_data_for_packaging_needed()

        # INFERIOR --> Only one packaging needed and shoudl be PACKAGING_1
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=5,
            unit=MeasurementUnit.ML.value
        )

        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])

        # EQUAL --> Only one packaging needed and shoudl be PACKAGING_1
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=self.packaging_1.quantity,
            unit=MeasurementUnit.ML.value
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

    def test_packaging_needed__many(self):
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

    def test_packaging_needed_drop(self):
        print("\n\ntest_packaging_needed_drop  --> START\n")

        product_drop_to_ml = Decimal('0.05')

        quantity = 10 * product_drop_to_ml
        self.packaging_1 = Packaging.objects.create(
            product=self.product,
            quantity=Decimal(format(quantity, ".2f")),
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )

        quantity = 20 * product_drop_to_ml
        self.packaging_2 = Packaging.objects.create(
            product=self.product,
            quantity=Decimal(format(quantity, ".2f")),
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )
        print("packaging 1 :", self.packaging_1)
        print("packaging 2 :", self.packaging_2)

        # INFERIOR --> Only one packaging needed and shoudl be PACKAGING_1
        print("-- INFERIOR --")
        quantity = 5
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=Decimal(format(quantity, ".2f")),
            unit=MeasurementUnit.GOUTTE
        )
        print("Packaging Need :", rq.packagings_needed)

        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])

        # EQUAL --> Only one packaging needed and shoudl be PACKAGING_1
        print("-- EQUAL --")
        quantity = 10
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=Decimal(format(quantity, ".2f")),
            unit=MeasurementUnit.GOUTTE
        )

        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_1, rq.packagings_needed[0])

        # SUPERIOR --> Only one packaging needed and shoudl be PACKAGING_2
        print("-- SUPERIOR --")
        quantity = 15
        rq = RecipeQuantity.objects.create(
            recipe=self.recipe,
            product=self.product,
            _quantity=Decimal(format(quantity, ".2f")),
            unit=MeasurementUnit.GOUTTE
        )
        print("----------------------------------> rq._quantity type :", type(rq.quantity))

        self.assertEqual(1, len(rq.packagings_needed))
        self.assertEqual(self.packaging_2, rq.packagings_needed[0])
        print("\ntest_packaging_needed_goutte  --> END\n\n")


# ==========
# AROMA USER
# ==========
class AromaUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create User
        user = User.objects.create_user(
            username="hello",
            email="test@test.com",
            password="password"
        )
        AromaUser.objects.create(
            user=user
        )

    def generate_optimize_basket_base_data(self):
        # Get User
        self.user = AromaUser.objects.get(id=1)

        # Create CATEGORY
        category = Category.objects.create(
            code=FunctionnalCategoryChoice.ARGILE,
            label="Categorie_1",
            parent=None
        )

        # Create PRODUCTS
        self.product_1 = Product.objects.create(
            label="product_1",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        self.product_2 = Product.objects.create(
            label="product_2",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        self.product_3 = Product.objects.create(
            label="product_3",
            category=category,
            containers_flag=ContainerFlag.NONE.value,
            product_details_flag=ProductDetailsFlag.NONE.value,
            url=FAKE_URL
        )

        # Create PACKAGING
        # -- Product_1
        self.packaging_product_1__1 = Packaging.objects.create(
            product=self.product_1,
            quantity=15,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

        self.packaging_product_1__2 = Packaging.objects.create(
            product=self.product_1,
            quantity=30,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )

        # -- Product_2
        self.packaging_product_2__1 = Packaging.objects.create(
            product=self.product_2,
            quantity=30,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

        self.packaging_product_2__2 = Packaging.objects.create(
            product=self.product_2,
            quantity=50,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )

        # -- Product 3
        self.packaging_product_3__1 = Packaging.objects.create(
            product=self.product_3,
            quantity=10,
            unit=MeasurementUnit.ML.value,
            price=DEFAULT_PRICE
        )

        self.packaging_product_3__2 = Packaging.objects.create(
            product=self.product_3,
            quantity=20,
            unit=MeasurementUnit.ML,
            price=DEFAULT_PRICE
        )

        # Create RECIPE
        self.recipe_1 = Recipe.objects.create(
            label="recipe_1",
            container_type=ContainerFlag.POT.value,
            conservation=3,
            final_quantity=30,
            final_unit=MeasurementUnit.ML.value,
            level=Recipe.Level.STARTER,
            properties_flag=PropertiesFlag.NONE.value,
            time=10,
            url=FAKE_URL
        )

        self.recipe_2 = Recipe.objects.create(
            label="recipe_2",
            container_type=ContainerFlag.POT.value,
            conservation=3,
            final_quantity=30,
            final_unit=MeasurementUnit.ML.value,
            level=Recipe.Level.STARTER,
            properties_flag=PropertiesFlag.NONE.value,
            time=10,
            url=FAKE_URL
        )

        # Create RECIPE QUANTITIES
        rq_1_1 = RecipeQuantity.objects.create(
            recipe=self.recipe_1,
            product=self.product_1,
            _quantity=10,
            unit=MeasurementUnit.ML
        )

        rq_1_2 = RecipeQuantity.objects.create(
            recipe=self.recipe_1,
            product=self.product_2,
            _quantity=25,
            unit=MeasurementUnit.ML
        )

        rq_2_2 = RecipeQuantity.objects.create(
            recipe=self.recipe_2,
            product=self.product_2,
            _quantity=20,
            unit=MeasurementUnit.ML
        )

        rq_2_3 = RecipeQuantity.objects.create(
            recipe=self.recipe_2,
            product=self.product_3,
            _quantity=30,
            unit=MeasurementUnit.ML
        )

    # ---------------
    # optimize_basket
    # ---------------
    def test_optimize_basket__recipe_1(self):
        print("\n\ntest_optimize_basket__recipe_1  --> START\n")
        self.generate_optimize_basket_base_data()

        # Add only recipe_1 to basket
        rb = RecipeBasket.objects.create(
            user=self.user,
            recipe=self.recipe_1,
            quantity=1
        )
        assert rb

        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)


        self.user.optimize_basket()

        basket = ProductBasket.objects.all()
        expected_packaging = self.recipe_1.get_all_packaging_needed()

        self.assertEqual(len(basket), len(expected_packaging))

        for i in range(len(expected_packaging)):
            self.assertEqual(basket[i].packaging, expected_packaging[i])

        print("\ntest_optimize_basket__recipe_1 --> END\n\n")

    def test_optimize_basket__recipe_1_recipe_2(self):
        print("\n\ntest_optimize_basket__recipe_1_recipe_2  --> START\n")
        self.generate_optimize_basket_base_data()

        # Add recipe_1 and recipe_2 to basket
        rb = RecipeBasket.objects.create(
            user=self.user,
            recipe=self.recipe_1,
            quantity=1
        )
        assert rb

        rb_2 = RecipeBasket.objects.create(
            user=self.user,
            recipe=self.recipe_2,
            quantity=1
        )
        assert rb_2

        # basket is empty to start
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        self.user.optimize_basket()

        basket = ProductBasket.objects.all()

        no_optimization_packagings = self.recipe_1.get_all_packaging_needed()
        no_optimization_packagings.extend(self.recipe_2.get_all_packaging_needed())
        self.assertNotEqual(len(basket), len(no_optimization_packagings))

        print("NON OPTIMIZATION :", no_optimization_packagings)

        expected_packaging = [
            self.packaging_product_1__1,
            self.packaging_product_2__2,
            self.packaging_product_3__2,
            self.packaging_product_3__1
        ]
        print("EXPECTATION :", expected_packaging)
        self.assertEqual(len(basket), len(expected_packaging))

        for i in range(len(expected_packaging)):
            self.assertEqual(basket[i].packaging, expected_packaging[i])

        print("\ntest_optimize_basket__recipe_1_recipe_2 --> END\n\n")

    def test_optimize_basket__recipe_1_x2_recipe_2(self):
        print("\n\ntest_optimize_basket__recipe_1_x2_recipe_2  --> START\n")
        self.generate_optimize_basket_base_data()

        # Add recipe_1 x 2 and recipe_2 to basket
        rb = RecipeBasket.objects.create(
            user=self.user,
            recipe=self.recipe_1,
            quantity=2
        )
        assert rb

        rb_2 = RecipeBasket.objects.create(
            user=self.user,
            recipe=self.recipe_2,
            quantity=1
        )
        assert rb_2

        # basket is empty to start
        basket = ProductBasket.objects.all()
        self.assertEqual(len(basket), 0)

        self.user.optimize_basket()

        basket = ProductBasket.objects.all()

        expected_packaging = [
            self.packaging_product_1__2,
            self.packaging_product_2__2,
            self.packaging_product_2__1,
            self.packaging_product_3__2,
            self.packaging_product_3__1
        ]
        print("EXPECTATION :", expected_packaging)
        self.assertEqual(len(basket), len(expected_packaging))

        for i in range(len(expected_packaging)):
            self.assertEqual(basket[i].packaging, expected_packaging[i])

        print("\ntest_optimize_basket__recipe_1_x2_recipe_2 --> END\n\n")

