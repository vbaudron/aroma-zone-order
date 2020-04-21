from django.core.management import BaseCommand

from myapp.models import Product, Category, CategoryChoice


# ==========
# CATEGORIES
# ==========
class Command(BaseCommand):

    def handle(self, *args, **options):
        self.populate_categories()

    category_hierarchy = {
        "None": [
            CategoryChoice.INGREDIENT_COSMETIQUE,
            CategoryChoice.CONTAINER,
            CategoryChoice.MATERIEL_FABRICATION
        ],
        CategoryChoice.INGREDIENT_COSMETIQUE: [
            CategoryChoice.ACTIF_COSMETIQUE,
            CategoryChoice.HUILE_VEGETALE,
            CategoryChoice.HYDROLAT,
            CategoryChoice.HUILE_ESSENTIELLE,
            CategoryChoice.CIRE_GOMME,
            CategoryChoice.EMULSIFIANT_EPAISSISSANT,
            CategoryChoice.AJUSTATEUR_PH,
            CategoryChoice.AGENT_LAVANT_MOUSSANT,
            CategoryChoice.CONSERVATEUR_ANTIOXI,
            CategoryChoice.MASQUE_GOMMAGE,
            CategoryChoice.COLORANT_POUDRE,
            CategoryChoice.PARFUM_NATUREL,
            CategoryChoice.SAVON_GLYCERINE,
            CategoryChoice.AGENT_MULTI_USE
        ],
        CategoryChoice.CONTAINER: [
            CategoryChoice.POT,
            CategoryChoice.FLACON
        ],
        CategoryChoice.MATERIEL_FABRICATION: [
            CategoryChoice.MATERIEL_DOSAGE_TRANSFERT,
            CategoryChoice.MATERIEL_MELANGE,
            CategoryChoice.MATERIEL_MAQUILLAGE
        ]
    }

    def get_parent_code(self, elem: CategoryChoice):
        for parent, children in self.category_hierarchy.items():
            if elem in children:
                return parent if isinstance(parent, CategoryChoice) else None

    def populate_categories(self):
        # Create Categories
        for elem in CategoryChoice:
            # get parent id
            parent_code = self.get_parent_code(elem)
            parent_id = None
            if parent_code:
                parent_id = Category.objects.get(code=parent_code)
            # Create Object
            Category.objects.create(
                code=elem.value,
                label=elem.label,
                parent_id=parent_id
            )
        print("Category Table populated")
