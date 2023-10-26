from django.shortcuts import render
from catalog.models import Product, Contact


# Create your views here.
def home_page(request):
    products = Product.objects.all()[:5]
    if request.method == 'GET':
        for product in products:
            print(product)
    return render(request, 'catalog/home_page.html')


def contact(request):
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
