from catalog.views import HomeListView, contacts, ProductListView, ProductCreateView, ProductDetailView
from django.urls import path
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('add/', ProductCreateView.as_view(), name='user_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='view_product')
]
