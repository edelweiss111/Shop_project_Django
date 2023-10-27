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
        'first_string': {'name': contacts[0].name, 'email': contacts[0].email, 'post': contacts[0].post},
        'second_string': {'name': contacts[1].name, 'email': contacts[1].email, 'post': contacts[1].post}
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a message from {name}({phone}): {message}')
    return render(request, 'catalog/contact.html', context=data)
