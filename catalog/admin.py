from django.contrib import admin
from catalog.models import Product, Category, Contact, Version


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка отображения модели Product"""
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    """Админка отображения модели Category"""
    list_display = ('id', 'name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Contact"""
    list_display = ('id', 'name', 'email')


@admin.register(Version)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Version"""
    list_display = ('id', 'name', 'number')
