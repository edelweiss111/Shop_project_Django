from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from catalog.models import Product, Contact


# Create your views here.
class HomeListView(ListView):
    """Контроллер домашней страницы"""
    model = Product

    template_name = 'catalog/home_list.html'


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.all()
        queryset = list(reversed(queryset))

        return queryset[:5]


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


class ProductListView(ListView):
    """Контроллер страницы товаров"""
    model = Product
    paginate_by = 6


class ProductCreateView(CreateView):
    """Контроллер страницы добавления товара от пользователя"""
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:products')


class ProductDetailView(DetailView):
    model = Product
