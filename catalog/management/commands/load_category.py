from django.core.management import BaseCommand
from catalog.models import Category
from config.settings import DATA
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Команда загрузки данных в таблицу Category"""
        with open(DATA, encoding='utf-8') as file:
            category_to_load = []
            data = json.load(file)

            for item in data:
                if item['model'] == 'catalog.category':
                    category_to_load.append(
                        Category(**item['fields'])
                    )
        Category.objects.bulk_create(category_to_load)