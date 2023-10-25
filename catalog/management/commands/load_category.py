from django.core.management import BaseCommand
from catalog.models import Category
from config.settings import DATA
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(DATA, encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item['model'] == 'catalog.category':
                    Category.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        description=item['fields']['description']
                    )
