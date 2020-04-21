from django.core.management import BaseCommand
from django.db import models
from myapp.models import Category


class Command(BaseCommand):

    def delete_rows_in(self, model: models.Model):
        print("Deleting {}".format(model.__name__))
        model.objects.all().delete()
        queryset = model.objects.all()
        if len(queryset) == 0:
            print("{} data has been deleted".format(model.__name__))
        else:
            print("something when wrong, {} has not been deleted :".format(model.__name__))
            print(queryset)


    def delete_categories_entries(self):
        print("Deleting categories")
        Category.objects.all().delete()

    def delete_all(self):
        # categories
        self.delete_rows_in(Category)

    def handle(self, *args, **options):
        answer = input("Are you sure you want to delete all data ? (Yes to confirm) ")
        if answer.upper() == "YES":
            self.delete_all()
