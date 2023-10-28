from catalog.views import home_page, contact, product
from django.urls import path
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contact, name='contact'),
    path('products/', product, name='product')
]
