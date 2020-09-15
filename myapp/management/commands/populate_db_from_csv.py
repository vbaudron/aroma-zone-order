from decimal import Decimal
from enum import Enum
from openpyxl import load_workbook
import os
from aroma_zone_order.settings import STATIC_ROOT

from django.core.management import BaseCommand

from myapp.models import Product, Category, MenuCategoryChoice, FunctionnalCategoryChoice, RecipeQuantity, Recipe, \
    Packaging, ContainerFlag, ProductDetailsFlag, PropertiesFlag, MeasurementUnit

menu_category_hierarchy = {
    "None": [
        MenuCategoryChoice.EXTRAIT_NATUREL,
        MenuCategoryChoice.INGREDIENT_COSMETIQUE,
        MenuCategoryChoice.CONTAINER,
        MenuCategoryChoice.MATERIEL_FABRICATION
    ],
    MenuCategoryChoice.EXTRAIT_NATUREL: [
        MenuCategoryChoice.HUILE_ESSENTIELLE,
        MenuCategoryChoice.ABSOLUE,
        MenuCategoryChoice.EXTRAIT_CO2,
        MenuCategoryChoice.HYDROLAT,
        MenuCategoryChoice.HUILE_VEGETALE,
        MenuCategoryChoice.GET_ALOE_VERA,
        MenuCategoryChoice.EXTRAIT_PLANTE_LIQUIDE,
        MenuCategoryChoice.EXTRAIT_RUCHE,
        MenuCategoryChoice.EXTRAIT_MARIN,
        MenuCategoryChoice.ARGILE,
        MenuCategoryChoice.SEL
    ],
    MenuCategoryChoice.INGREDIENT_COSMETIQUE: [
        MenuCategoryChoice.ACTIF_COSMETIQUE,
        MenuCategoryChoice.CIRE_GOMME,
        MenuCategoryChoice.EMULSIFIANT_EPAISSISSANT,
        MenuCategoryChoice.AJUSTATEUR_PH,
        MenuCategoryChoice.AGENT_LAVANT_MOUSSANT,
        MenuCategoryChoice.CONSERVATEUR_ANTIOXI,
        MenuCategoryChoice.MASQUE_GOMMAGE,
        MenuCategoryChoice.COLORANT_POUDRE,
        MenuCategoryChoice.PARFUM_NATUREL,
        MenuCategoryChoice.SAVON_GLYCERINE,
        MenuCategoryChoice.AGENT_MULTI_USE
    ],
    MenuCategoryChoice.CONTAINER: [
        MenuCategoryChoice.POT,
        MenuCategoryChoice.FLACON
    ],
    MenuCategoryChoice.MATERIEL_FABRICATION: [
        MenuCategoryChoice.MATERIEL_DOSAGE_TRANSFERT,
        MenuCategoryChoice.MATERIEL_MELANGE,
        MenuCategoryChoice.MATERIEL_MAQUILLAGE
    ]
}

functionnal_category_hierachy = {
    "NONE": [
        FunctionnalCategoryChoice.INGREDIENT_COSMETIQUE,
        FunctionnalCategoryChoice.CONTAINER,
        FunctionnalCategoryChoice.MATERIEL_FABRICATION
    ],
    FunctionnalCategoryChoice.INGREDIENT_COSMETIQUE: [
        FunctionnalCategoryChoice.HUILE_BEURRE_VEGETAL,
        FunctionnalCategoryChoice.HYDROLAT,
        FunctionnalCategoryChoice.HUILE_ESSENTIELLE,
        FunctionnalCategoryChoice.ACTIF_COSMETIQUE,
        FunctionnalCategoryChoice.POUDRE_PLANTE,
        FunctionnalCategoryChoice.EXTRAIT_PLANTE,
        FunctionnalCategoryChoice.FRAGRANCE_NATURELLE,
        FunctionnalCategoryChoice.EXFOLIANT_NATUREL,
        FunctionnalCategoryChoice.ARGILE,
        FunctionnalCategoryChoice.COLORANT,
        FunctionnalCategoryChoice.EMOLIENT,
        FunctionnalCategoryChoice.AGENT_DE_TEXTURE,
        FunctionnalCategoryChoice.TENSIOACTIF,
        FunctionnalCategoryChoice.EMULSIFIANT,
        FunctionnalCategoryChoice.CONSERVATEUR,
        FunctionnalCategoryChoice.ANTIOXYDANT,
        FunctionnalCategoryChoice.AJUSTATEUR_PH,
        FunctionnalCategoryChoice.BASE_NEUTRE
    ],
    FunctionnalCategoryChoice.HUILE_BEURRE_VEGETAL: [
        FunctionnalCategoryChoice.HUILE_VEGETALE,
        FunctionnalCategoryChoice.BEURRE_VETEAL,
        FunctionnalCategoryChoice.MACREAT_HUILEUX
    ],
    FunctionnalCategoryChoice.AGENT_DE_TEXTURE: [
        FunctionnalCategoryChoice.CIRE,
        FunctionnalCategoryChoice.GOMME,
        FunctionnalCategoryChoice.ALCOOL_GRAS
    ],
    FunctionnalCategoryChoice.CONTAINER: [
        FunctionnalCategoryChoice.POT,
        FunctionnalCategoryChoice.FLACON
    ],
    FunctionnalCategoryChoice.MATERIEL_FABRICATION: [
        FunctionnalCategoryChoice.MATERIEL_DOSAGE_TRANSFERT,
        FunctionnalCategoryChoice.MATERIEL_MELANGE,
        FunctionnalCategoryChoice.MATERIEL_MAQUILLAGE
    ]
}


# ==========
# CATEGORIES
# ==========

class MyXLS:
    NAME = "populate_test_basic.xlsx"

    class Sheet(Enum):
        RECIPE = Recipe
        PRODUCT = Product
        QUANTITY = RecipeQuantity
        PACKAGING = Packaging

        @property
        def sheet_name(self):
            return self.name.lower()


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.wb = load_workbook(os.path.join(STATIC_ROOT, MyXLS.NAME))

    def get_parent_code(self, elem: FunctionnalCategoryChoice):
        for parent, children in functionnal_category_hierachy.items():
            if elem in children:
                return parent if isinstance(parent, FunctionnalCategoryChoice) else None

    def populate_categories(self):
        # Create Categories
        for elem in FunctionnalCategoryChoice:
            # get parent id
            parent_code = self.get_parent_code(elem)
            parent = None
            if parent_code:
                parent = Category.objects.get(code=parent_code)
                print(elem, " has parent_code :", parent_code, "found parent :", parent)
            # Create Object
            obj = Category.objects.create(
                code=elem.value,
                label=elem.label.lower(),
                parent=parent
            )
            print("Category {} : {} created with parent : {}".format(
                obj.id,
                elem.label,
                FunctionnalCategoryChoice(parent_code) if parent_code else "None"
            ))
        print("populate categories DONE")

    def populate_product_from_csv(self):
        print("populate PRODUCT ...")
        print("____________________________________")
        # Product
        sheet = self.wb["product"]
        sheet.delete_rows(sheet.min_row, 1)  # delete first row (name)

        for row in sheet.values:
            if row[0] is None:
                print("break with row :", row)
                break
            print("row :", row)
            category = Category.objects.get(label=row[0].lower())
            density = Decimal(format(row[2], ".2f")) if row[2] else row[2]
            ml_to_goutte = Decimal(format(row[3], ".2f")) if row[3] else row[3]
            Product.objects.create(
                label=row[1].lower(),
                category=category,
                containers_flag=ContainerFlag.NONE.value,
                product_details_flag=ProductDetailsFlag.NONE.value,
                properties_flag=PropertiesFlag.NONE.value,
                url=row[4],
                density=density,
                ml_to_goutte=ml_to_goutte
            )
        print("populate products DONE")

    def populate_recipe_from_csv(self):
        print("populate RECIPES ...")
        print("____________________________________")
        # Product
        sheet = self.wb["recipe"]
        sheet.delete_rows(sheet.min_row, 1)  # delete first row (name)

        for row in sheet.values:
            if row[0] is None:
                print("break with row :", row)
                break
            print("row :", row)
            container = ContainerFlag[row[3].upper()]
            unit = MeasurementUnit[row[2].upper()]
            level = Recipe.Level[row[5].upper()]
            Recipe.objects.create(
                label=row[0],
                container_type=container.value,
                conservation=row[4],
                final_quantity=row[1],
                final_unit=unit,
                level=level,
                properties_flag=PropertiesFlag.NONE.value,
                time=row[6],
                url=row[7]
            )
        print("populate recipes DONE")

    def populate_recipe_quantity(self):
        print("populate QUANTITIES ...")
        print("____________________________________")
        # Product
        sheet = self.wb["quantity"]
        sheet.delete_rows(sheet.min_row, 1)  # delete first row (name)

        for row in sheet.values:
            if row[0] is None:
                print("break with row :", row)
                break
            print("row :", row)
            recipe = Recipe.objects.get(label=row[0])
            product = Product.objects.get(label=row[1])
            quantity = Decimal(format(row[2], ".2f"))
            unit = MeasurementUnit[row[3].upper()]
            RecipeQuantity.objects.create(
                recipe=recipe,
                product=product,
                _quantity=quantity,
                unit=unit
            )

        print("populate quantities DONE")


    def populate_packaging(self):
        print("populate PACKAGING ...")
        print("____________________________________")
        # Product
        sheet = self.wb["packaging"]
        sheet.delete_rows(sheet.min_row, 1)  # delete first row (name)

        for row in sheet.values:
            if row[0] is None:
                print("break with row :", row)
                break
            print("row :", row)
            product = Product.objects.get(label=row[0])
            unit = MeasurementUnit[row[1].upper()]
            quantity = format(row[2], ".2f")
            price = Decimal(format(row[3], ".2f"))
            Packaging.objects.create(
                product=product,
                quantity=quantity,
                unit=unit,
                price=price
            )
        print("populate packaging DONE")

    def handle(self, *args, **options):
        self.populate_categories()
        print("/n____________________________________")
        self.populate_product_from_csv()
        print("/n____________________________________")
        self.populate_recipe_from_csv()
        print("/n____________________________________")
        self.populate_packaging()
        print("/n____________________________________")
        self.populate_recipe_quantity()
