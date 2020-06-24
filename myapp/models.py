import logging as log
from abc import ABC

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from enum import auto, Flag, unique, Enum


# =============
# Flags & Enums
# =============

# ---------------
# MeasurementUnit
# ---------------


class MeasurementUnit(models.IntegerChoices):
    NONE = 0
    ML = auto()
    GRAMS = auto()
    GOUTTE = auto()
    MASQUE = auto()

MEASUREMENT_UNIT_LEN_MAX = 6


# --------
# Category
# --------

class FunctionnalCategoryChoice(models.IntegerChoices):
    # -- PARENT --
    INGREDIENT_COSMETIQUE = auto()
    # elem
    HUILE_BEURRE_VEGETAL = auto()
    ## children
    HUILE_VEGETALE = auto()
    BEURRE_VETEAL = auto()
    MACREAT_HUILEUX = auto()
    # elem (re)
    HYDROLAT = auto()
    HUILE_ESSENTIELLE = auto()
    ACTIF_COSMETIQUE = auto()
    POUDRE_PLANTE = auto()
    EXTRAIT_PLANTE = auto()
    FRAGRANCE_NATURELLE = auto()
    EXFOLIANT_NATUREL = auto()
    ARGILE = auto()
    COLORANT = auto()
    EMOLIENT = auto()
    AGENT_DE_TEXTURE = auto()
    ## children
    CIRE = auto()
    GOMME = auto()
    ALCOOL_GRAS = auto()
    # elem (re)
    TENSIOACTIF = auto()
    EMULSIFIANT = auto()
    CONSERVATEUR = auto()
    ANTIOXYDANT = auto()
    AJUSTATEUR_PH = auto()
    # ---
    BASE_NEUTRE = auto()

    # -- PARENT --
    CONTAINER = auto()
    # elem
    POT = auto()
    FLACON = auto()

    # -- PARENT --
    MATERIEL_FABRICATION = auto()
    # elem
    MATERIEL_DOSAGE_TRANSFERT = auto()
    MATERIEL_MELANGE = auto()
    MATERIEL_MAQUILLAGE = auto()

# UNUSED
class   MenuCategoryChoice(models.IntegerChoices):
    # -- CAT 1 --
    EXTRAIT_NATUREL = auto()
    # elem
    HUILE_ESSENTIELLE = auto()
    ABSOLUE = auto()
    EXTRAIT_CO2 = auto()
    HYDROLAT = auto()
    HUILE_VEGETALE = auto()
    BEURRE_VEGETAUX = auto()
    GET_ALOE_VERA = auto()
    EXTRAIT_PLANTE_LIQUIDE = auto()
    EXTRAIT_RUCHE = auto()
    EXTRAIT_MARIN = auto()
    VINAIGRE_NATUREL = auto()
    ARGILE = auto()
    SEL = auto()

    # -- CAT 2 --
    INGREDIENT_COSMETIQUE = auto()
    # elem
    ACTIF_COSMETIQUE = auto()
    CIRE_GOMME = auto()
    EMULSIFIANT_EPAISSISSANT = auto()
    AJUSTATEUR_PH = auto()
    AGENT_LAVANT_MOUSSANT = auto()
    CONSERVATEUR_ANTIOXI = auto()
    MASQUE_GOMMAGE = auto()
    COLORANT_POUDRE = auto()
    PARFUM_NATUREL = auto()
    SAVON_GLYCERINE = auto()
    AGENT_MULTI_USE = auto()

    # -- CAT 3 --
    CONTAINER = auto()
    # elem
    POT = auto()
    FLACON = auto()

    # -- CAT 4 --
    MATERIEL_FABRICATION = auto()
    # elem
    MATERIEL_DOSAGE_TRANSFERT = auto()
    MATERIEL_MELANGE = auto()
    MATERIEL_MAQUILLAGE = auto()

    # -- CAT 5 --
    COSMETIQUE_NATUREL_BIO = auto()
    # elem
    SOIN_CORPS_VISAGE_BIO = auto()
    SOIN_CHEVEUX_BIO = auto()
    SOIN_LAVANT_DEO_BIO = auto()
    MAQUILLAGE_BIO = auto()
    BASE_NEUTRE_BIO = auto()


    #TODO Coffret


# -------
# Product
# -------


class ContainerFlag(Flag, models.IntegerChoices):
    NONE = 0
    # -- function --
    POT = auto()
    FLACON_SIMPLE = auto()
    FLACON_DENTIFRICE = auto()
    FLACON_ROLL_ON = auto()
    FLACON_MOUSSEUR = auto()
    FLACON_COMPTE_GOUTTE = auto()
    FLACON_SPRAY = auto()
    FLACON_CREME = auto()
    FLACON_SAVON = auto()
    FLACON_APPLICATEUR = auto()
    ETUI_STICK = auto()
    ETUI_LEVRE = auto()
    FLACON_TWISTER = auto()
    # -- part --
    BOUCHON = auto()
    BASE = auto()
    # -- divers --
    AIRLESS = auto()


class ProductDetailsFlag(Flag):
    NONE = 0
    # -- color --
    RED = auto()
    BLUE = auto()
    VIOLET = auto()
    ORANGE = auto()
    PINK = auto()
    AMBER = auto()
    WHITE = auto()
    BLACK = auto()
    SILVER = auto()
    # -- opacité --
    TRANSPARENT = auto()
    DEPOLI = auto()
    OPAQUE = auto()
    # -- matière --
    PET = auto()
    PET_RECYCLE = auto()
    VERRE = auto()
    ALUMINIUM = auto()
    PLASTIQUE = auto()
    # -- forme --
    TUBE = auto()
    ROND = auto()
    PRISME = auto()


class PropertiesFlag(Flag):
    NONE = 0
    EXFOLIANT = auto()
    PURIFIANT = auto()
    DESALTERANT = auto()
    ADOUCISSANT = auto()
    NUTRITIF = auto()
    DETOX = auto()
    REPARATEUR = auto()
    PROTECTEUR_EMOLIANT = auto()
    APAISANT = auto()
    ZONE_CICATRICIELLE = auto()
    FRAICHEUR = auto()
    ANTI_AGE = auto()
    SEBOREGULATEUR = auto()


# ===============
# ABSTRACTS Class
# ===============

class MeasurementUnitModelBased:
    __measurement_unit: MeasurementUnit

    def __init__(self):
        self._call_define_measurement_unit()

    def _define_measurement_unit(self, unit_value):
        self.__measurement_unit = MeasurementUnit(unit_value)

    def _call_define_measurement_unit(self):
        raise NotImplementedError

    @property
    def measurement_unit(self):
        return self.__measurement_unit


# ==============
# DB TABLE MODEL
# ==============

# ---------------
# FIELDS Creation
# ---------------

class MeasurementUnitFields(models.PositiveSmallIntegerField):

    description = "A field to add a MeasurementUnit value"

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = MeasurementUnit.choices
        kwargs['default'] = MeasurementUnit.NONE
        super().__init__(*args, **kwargs)


# --------------
# MODELS Creation
# --------------

class AromaUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def optimize_basket(self):
        """ Try to minimise number of packaging for each product needed in all recipe and handle Stock if there is
        quantity_per_product will be created :
        {
            "product_1": [{
                "unit": MeasurementUnit_1,
                "quantity": sum of quantity
            },
            {
                "unit": MeasurementUnit_2,
                "quantity": sum of quantity
            }],
            ...
        }
        TODO 2 different units for same products shoudn't exist, does it ?
        We
        """
        # Simple QUERY because can not group by product and add quantity in case unit is different
        basket_recipes = RecipeBasket.objects.filter(user=self)
        print("basket :", basket_recipes)

        quantity_needed = dict()
        # Handle RECIPE BASKET
        for recipe_basket in basket_recipes:
            print("--------- RECIPE :", recipe_basket, "quantity :", recipe_basket.quantity)
            ingredients = recipe_basket.recipe.ingredients.all()
            for recipe_quantity in ingredients:
                print("---- recipe_quantity :", recipe_quantity)
                if recipe_quantity.product not in quantity_needed.keys():
                    quantity_needed[recipe_quantity.product] = list()
                    print("product not in key --> created :", quantity_needed[recipe_quantity.product])
                unit_list = quantity_needed[recipe_quantity.product]
                print("** unit_list definition ** --> ", unit_list)
                print("try to find :", recipe_quantity.measurement_unit.name)
                try:
                    idx = next(index for (index, d) in enumerate(unit_list) if d["unit"] == recipe_quantity.measurement_unit.name)
                    print("'{}' NOT FOUND in {} at idx {}".format(recipe_quantity.measurement_unit.name, unit_list, idx))
                    print("before :", unit_list[idx])
                    unit_list[idx]["quantity"] += (recipe_quantity.quantity * recipe_basket.quantity)
                    print("after :", unit_list[idx])
                except StopIteration:
                    print("{} NOT FOUND in {}".format(recipe_quantity.measurement_unit.name, unit_list))
                    unit_list.append({
                        "unit": recipe_quantity.measurement_unit.name,
                        "quantity": (recipe_quantity.quantity * recipe_basket.quantity)
                    })
                    print("created :", unit_list[len(unit_list) - 1])
        #      if not any(d["unit"] == recipe_quantity.measurement_unit for d in unit_list):
        print("\n1. quantity_needed :", quantity_needed)

        # Handle EXTRA QUANTITY WANTED

        # Handle Stock
        stock = UserStock.objects.filter(user=self)

        # Get pertinent packagings for needed quantities
        full_packaging = list()
        for product, data in quantity_needed.items():
            packagings_to_add = list()  #  TODO (A): removed to directly add to full packaging
            data = data[0]
            print("\nPRODUCT {}  DATA {}".format(product, data))
            #TODO : MAKE IT CLEARED. Here supposed that ONLY ONE UNIT PER PRODUCT
            quantity_to_handle = data["quantity"]
            while quantity_to_handle > 0:
                pack_to_add = product.get_smallest_satisfying_packaging(
                    quantity=quantity_to_handle,
                    unit=MeasurementUnit[data["unit"]]
                )
                if pack_to_add:
                    packagings_to_add.append(pack_to_add) #  TODO (A): removed to directly add to full packaging
                    quantity_to_handle -= pack_to_add.quantity
                    full_packaging.append(pack_to_add)
                else:
                    # TODO define what to do
                    import pdb;pdb.set_trace()
            print("For {} {} of PRODUCT {} packagings needed are : {}".format(data["quantity"], data["unit"], product, packagings_to_add))

        print("\n2. Packaging to add :", full_packaging)
        # Add Packagings to ProductBasket
        for packaging in full_packaging:
            ProductBasket.objects.create(
                user=self,
                packaging=packaging
            )
            print(packaging, "has been added to basket")





    def __str__(self):
        return self.user.username


# TODO --> [QUESTION] : Product Category --> Many To ONE ?

class Category(MPTTModel):
    code = models.IntegerField(choices=FunctionnalCategoryChoice.choices)
    label = models.CharField(max_length=25, null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['label']
        
    def __str__(self):
        return self.label


class Product(models.Model):
    label = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    containers_flag = models.IntegerField(default=ContainerFlag.NONE.value)
    product_details_flag = models.IntegerField(default=ProductDetailsFlag.NONE.value)
    properties_flag = models.IntegerField(default=PropertiesFlag.NONE.value)
    url = models.URLField()
    
    def __str__(self):
        return self.label
    
    def get_smallest_satisfying_packaging(self, quantity=None, unit: MeasurementUnit=None):
        packagings = self.packagings.all()
        # print("get smallest satisfying packaging with quantity = {}".format(quantity))
        # [Question] Unit conversion --> for now all in ml and grams, liter and kg would be for front only
        
        smallest_satisfied = self.get_biggest_packaging()

        # TODO : How to handle when no packagings found
        if not smallest_satisfied:
            print("no packaging found for", self.label)
            return None

      #  print("biggest packaging found :", smallest_satisfied)
        # No need to loop if biggest cant_satisfied quantity
        if quantity is not None and smallest_satisfied.quantity < quantity:
            return smallest_satisfied
        
        # find smallest satisfying packaging
        for packaging in packagings:
            if not unit or unit == packaging.measurement_unit:
                try:
                    if packaging <= smallest_satisfied and (quantity is None or packaging.quantity >= quantity):
                        smallest_satisfied = packaging
                except MeasurementUnitComparaisonError as e:
                    message = "Product {} : {}".format(self, e)
                    log.debug(message)
            else:
                print("unit of packaging {} is not the same as asked ({})".format(packaging.measurement_unit, unit))

        return smallest_satisfied
    
    def get_biggest_packaging(self):
        packagings = self.packagings.all()
        biggest = None
        for packaging in packagings:
            try:
     #           print("compare pack : {} than biggest : {}".format(packaging, biggest))
                if packaging >= biggest:
                    biggest = packaging
        #            print("bigger")
            except MeasurementUnitComparaisonError as e:
                message = "Product {} : {}".format(self, e)
                log.debug(message)
        return biggest


class Recipe(models.Model, MeasurementUnitModelBased):

    class Level(models.IntegerChoices):
        STARTER = auto()
        ADVANCED = auto()
        CONFIRMED = auto()

    label = models.CharField(max_length=200)
    container_type = models.IntegerField(choices=ContainerFlag.choices)
    conservation = models.PositiveSmallIntegerField(null=False)  # MONTH
    final_quantity = models.PositiveIntegerField(null=False)
    final_unit = MeasurementUnitFields()
    level = models.IntegerField(choices=Level.choices, default=Level.STARTER.value)
    properties_flag = models.IntegerField(default=PropertiesFlag.NONE.value)
    time = models.PositiveSmallIntegerField()  # MINUTES
    url = models.URLField()

    def _call_define_measurement_unit(self):
        self._define_measurement_unit(self.final_unit)

    def add_to_basket(self, user: AromaUser):
        RecipeBasket.objects.create(user=user, recipe=self, quantity=1)

    def add_ingredients_to_basket(self, user: AromaUser):
        # Add PACKAGING to basket
        print("ADD {} TO BASKET".format(self.label))
        packaging_needed = self.get_all_packaging_needed()
        for packaging in packaging_needed:
            ProductBasket.objects.create(
                user=user,
                packaging=packaging
            )
            print("packaging '{}' is added to basket".format(packaging))

    def get_all_packaging_needed(self) -> list:
        all_packs = list()
        ingredients = self.ingredients.all()
        print("How to make {} recipe :".format(self))
        for ingredient in ingredients:
            print("Need", ingredient)
            for packaging in ingredient.packagings_needed:
                all_packs.append(packaging)
                print("packaging '{}' is added to needs".format(packaging))
        return all_packs

    def __str__(self):
        return self.label


class RecipeQuantity(models.Model, MeasurementUnitModelBased):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recipes")
    _quantity = models.FloatField(null=False, default=0)
    unit = MeasurementUnitFields()
    
    __packagings_needed: list()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__update_packagings_needed()
        
    def _call_define_measurement_unit(self):
        self._define_measurement_unit(self.unit)
        
    def __update_packagings_needed(self):
        self.__packagings_needed = list()
        quantity_to_handle = self._quantity
        while quantity_to_handle > 0:
            pack_to_add = self.product.get_smallest_satisfying_packaging(quantity=quantity_to_handle)
            if pack_to_add:
                self.__packagings_needed.append(pack_to_add)
                quantity_to_handle -= pack_to_add.quantity
            else:
                # TODO define what to do
                import pdb;pdb.set_trace()
                
    @property
    def packagings_needed(self):
        return self.__packagings_needed
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, new_quantity):
        self._quantity = new_quantity
        self.__update_packagings_needed()
        
    def __str__(self):
        message = "{} {} of {}".format(
            self._quantity,
            self.unit,
            self.product
        )
        return message


class Packaging(models.Model, MeasurementUnitModelBased):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="packagings")
    quantity = models.PositiveIntegerField()
    unit = MeasurementUnitFields()
    price = models.FloatField(null=False)

    def _call_define_measurement_unit(self):
        self._define_measurement_unit(self.unit)
        
    def __str__(self):
        my_str = "{} : {} {}".format(
            self.product.__str__(),
            self.quantity,
            self.measurement_unit.name
        )
        return my_str
    
    def __le__(self, packaging_to_compare):
        # nothing to compare with
        if not packaging_to_compare:
            return True
        # not the same unit to compare
        if self.unit != packaging_to_compare.unit:
            raise MeasurementUnitComparaisonError(self.unit, packaging_to_compare.unit)
        # comparaison
        return self.quantity <= packaging_to_compare.quantity

    def __lt__(self, packaging_to_compare):
        # nothing to compare with
        if not packaging_to_compare:
            return True
        # not the same unit to compare
        if self.unit != packaging_to_compare.unit:
            raise MeasurementUnitComparaisonError(self.unit, packaging_to_compare.unit)
        # comparaison
        return self.quantity < packaging_to_compare.quantity
    
    def __ge__(self, packaging_to_compare):
        # nothing to compare with
        if not packaging_to_compare:
            return True
        # not the same unit to compare
        if self.unit != packaging_to_compare.unit:
            raise MeasurementUnitComparaisonError(self.unit, packaging_to_compare.unit)
        # comparaison
        return self.quantity >= packaging_to_compare.quantity

    def __gt__(self, packaging_to_compare):
        # nothing to compare with
        if not packaging_to_compare:
            return True
        # not the same unit to compare
        if self.unit != packaging_to_compare.unit:
            raise MeasurementUnitComparaisonError(self.unit, packaging_to_compare.unit)
        # comparaison
        return self.quantity > packaging_to_compare.quantity


class ProductBasket(models.Model):
    user = models.ForeignKey(AromaUser, on_delete=models.CASCADE)
    packaging = models.ForeignKey(Packaging, on_delete=models.CASCADE)
  #  quantity = models.PositiveIntegerField()
        
    def __str__(self):
        return self.packaging.__str__()
    
    def __contains__(self, product: Product):
        print("IS {} IN {} ?".format(product, self))
        return True if self.packaging.product == product else False
        

class RecipeBasket(models.Model):
    user = models.ForeignKey(AromaUser, on_delete=models.CASCADE, related_name="basket_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.recipe.__str__()


class UserStock(models.Model, MeasurementUnitModelBased):
    user = models.ForeignKey(AromaUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=False, default=0)
    unit = MeasurementUnitFields()

    def _call_define_measurement_unit(self):
        self._define_measurement_unit(self.unit)
        
    def __str__(self):
        return self.product.label


class MeasurementUnitComparaisonError(Exception):

    def __init__(self, unit, unit_to_compare):
        self.__unit = unit
        self.__unit_to_compare = unit_to_compare
        
    def __str__(self):
        message = "{} and {} can not be compared".format(self.__unit, self.__unit_to_compare)
        return message
        

if __name__ == '__main__':
    import pdb; pdb.set_trace()
