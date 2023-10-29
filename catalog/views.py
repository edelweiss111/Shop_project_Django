from django.shortcuts import render
from catalog.models import Product, Contact, Category


# Create your views here.
def home_page(request):
    """Контроллер домашней страницы"""
    products_list = Product.objects.all()
    last_products = []
    for item in reversed(products_list):
        last_products.append(item)
    context = {
        'product_list': last_products[:5],
    }

    return render(request, 'catalog/home_page.html', context=context)


def contacts(request):
    """Контроллер страницы контактов"""
    contacts_list = Contact.objects.all()
    data = {
        'contact_list': contacts_list,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a message from {name}({phone}): {message}')
    return render(request, 'catalog/contact.html', context=data)


def products(request):
    """Контроллер страницы товаров"""
    products_list = Product.objects.all()
    context = {
        'product_list': products_list,
    }

    return render(request, 'catalog/products.html', context=context)


def user_product(request):
    """Контроллер страницы товаров"""
    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = 'products/' + request.POST.get('image')
        price = request.POST.get('price')
        category = Category.objects.get(name=request.POST.get('category'))
        print(f'1 - {name}, 2 - {description}, 3 - {image}, 4 - {price}, 5 - {category}')
        Product.objects.create(name=name, description=description, image=image, price=price, category=category)
    return render(request, 'catalog/user_product.html', context=context)
