from django.views.decorators.cache import cache_page

from catalog.views import HomeListView, ContactTemplateView, ProductListView, ProductCreateView, ProductDetailView, \
    ProductUpdateView, ProductDeleteView
from django.urls import path
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('add/', ProductCreateView.as_view(), name='user_product'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('products_delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
