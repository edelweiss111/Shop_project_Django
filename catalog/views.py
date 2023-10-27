from django.shortcuts import render
from catalog.models import Product, Contact


# Create your views here.
def home_page(request):
    """Контроллер домашней страницы"""
    products = Product.objects.all()
    last_products = []
    if request.method == 'GET':
        for product in reversed(products):
            last_products.append(product)
        for item in last_products[:5]:
            print(item)
    return render(request, 'catalog/home_page.html')


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
