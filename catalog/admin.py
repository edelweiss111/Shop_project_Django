from django.contrib import admin
from catalog.models import Product, Category, Contact, Blog, Version


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


@admin.register(Blog)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_added')


@admin.register(Version)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')
