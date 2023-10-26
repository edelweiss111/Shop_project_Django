from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Category.truncate_table_restart_id()
            Category.objects.all().delete()
            Product.truncate_table_restart_id()
            Product.objects.all().delete()
        except Exception as e:
            raise e

