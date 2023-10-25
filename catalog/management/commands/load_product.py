from django.core.management import BaseCommand
from catalog.models import Category, Product
from config.settings import DATA
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(DATA, encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item['model'] == 'catalog.product':
                    Product.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        description=item['fields']['description'],
                        image=item['fields']['image'],
                        category=Category.objects.get(id=item['fields']['category']),
                        date_added=item['fields']['date_added'],
                        date_modified=item['fields']['date_modified'],
                        price=item['fields']['price']
                    )
