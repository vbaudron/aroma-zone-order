from django.db import models
from django.contrib.auth.models import User
from enum import auto, Flag, unique, Enum


# =============
# Flags & Enums
# =============

# ---------------
# MeasurementUnit
# ---------------

@unique
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

class   CategoryChoice(models.IntegerChoices):
    # CAT 1
    INGREDIENT_COSMETIQUE = auto()
    # elem
    ACTIF_COSMETIQUE = auto()
    HUILE_VEGETALE = auto()
    HYDROLAT = auto()
    HUILE_ESSENTIELLE = auto()
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

    # CAT 2
    CONTAINER = auto()
    # -- elem --
    POT = auto()
    FLACON = auto()

    # CAT 3
    MATERIEL_FABRICATION = auto()
    # -- elem --
    MATERIEL_DOSAGE_TRANSFERT = auto()
    MATERIEL_MELANGE = auto()
    MATERIEL_MAQUILLAGE = auto()

    #TODO Coffret



# -------------
# Product Flags
# -------------

@unique
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


@unique
class ProductDetailsFlags(Flag):
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
    NONE = auto()
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


# ==============
# DB TABLE MODEL
# ==============

# TODO --> [QUESTION] : Product Category --> Many To ONE ?

class Category(models.Model):
    code = models.IntegerField(choices=CategoryChoice.choices)
    label = models.CharField(max_length=25, null=False)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Product(models.Model):
    label = models.CharField(max_length=200)
    unit = models.CharField(max_length=MEASUREMENT_UNIT_LEN_MAX, choices=MeasurementUnit.choices)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    containers_flag = models.IntegerField(default=ContainerFlag.NONE)
    product_details_flag = models.IntegerField(default=ProductDetailsFlags.NONE)
    properties_flag = models.IntegerField(default=PropertiesFlag.NONE)


class Recipe(models.Model):

    class Level(models.IntegerChoices):
        STARTER = auto()
        ADVANCED = auto()
        CONFIRMED = auto()

    label = models.CharField(max_length=200)
    container_type = models.IntegerField(choices=ContainerFlag.choices)
    conservation = models.PositiveSmallIntegerField(null=False)  # MONTH
    ingredients = models.ManyToManyField(Product, through='RecipeQuantity', related_name="recipes")
    final_quantity = models.PositiveIntegerField(null=False)
    level = models.IntegerField(choices=Level.choices, default=Level.STARTER)
    properties_flag = models.IntegerField(default=PropertiesFlag.NONE)
    time = models.PositiveSmallIntegerField()  # MINUTES


class RecipeQuantity(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=False, default=0)
    unit = models.IntegerField(choices=MeasurementUnit.choices, default=MeasurementUnit.ML)


class Packaging(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.SmallIntegerField(choices=MeasurementUnit.choices, default=MeasurementUnit.ML)
    price = models.FloatField(null=False)


class UserAroma(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductBasket(models.Model):
    user_id = models.ForeignKey(UserAroma, on_delete=models.CASCADE)
    packaging_id = models.ForeignKey(Packaging, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class RecipeBasket(models.Model):
    user_id = models.ForeignKey(UserAroma, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class UserStock(models.Model):
    user_id = models.ForeignKey(UserAroma, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=False, default=0)
    unit = models.IntegerField(choices=MeasurementUnit.choices, default=MeasurementUnit.ML)


if __name__ == '__main__':
    import pdb; pdb.set_trace()
