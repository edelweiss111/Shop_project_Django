from django.core.management import BaseCommand
from catalog.models import Category, Product
from config.settings import DATA
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Команда загрузки данных в таблицу Product"""
        with open(DATA, encoding='utf-8') as file:
            data = json.load(file)
            product_to_load = []
            for item in data:
                if item['model'] == 'catalog.product':
                    item['fields']['category'] = Category.objects.get(id=item['fields']['category'])
                    product_to_load.append(
                        Product(**item['fields'])
                    )
        Product.objects.bulk_create(product_to_load)
