from django.shortcuts import render
from catalog.models import Product, Contact


# Create your views here.
def home_page(request):
    """Контроллер домашней страницы"""
    products = Product.objects.all()
    last_products = []
    for item in reversed(products):
        last_products.append(item)
    context = {
        'product_list': last_products[:5],
    }

    return render(request, 'catalog/home_page.html', context=context)


def contact(request):
    """Контроллер страницы контактов"""
    contacts = Contact.objects.all()
    data = {
        'contact_list': contacts,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a message from {name}({phone}): {message}')
    return render(request, 'catalog/contact.html', context=data)


def product(request):
    """Контроллер страницы товаров"""
    products = Product.objects.all()
    context = {
        'product_list': products,
    }

    return render(request, 'catalog/product.html', context=context)
