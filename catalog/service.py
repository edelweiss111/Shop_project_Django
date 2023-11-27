from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_categories_from_cache():
    if settings.CACHE_ENABLED is True:
        key = 'categories'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def check_user(user, author):
    custom_perms = (
        'catalog.set_is_published',
        'catalog.set_category',
        'catalog.set_description'
    )
    if user == author or user.is_superuser is True:
        return True
    elif user.groups.filter(name='moderators').exists() and user.has_perms(custom_perms):
        return True
    return False
