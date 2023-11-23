from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView

from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from catalog.forms import ProductForm, VersionForm, ModeratorProductForm

from catalog.models import Product, Contact, Version


# Create your views here.
class HomeListView(LoginRequiredMixin, ListView):
    """Контроллер домашней страницы"""
    model = Product

    template_name = 'catalog/home_list.html'

    def get_queryset(self, *args, **kwargs):
        """Отображение только 5 последних добавленных товаров"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.all()
        queryset = list(reversed(queryset))

        return queryset[:5]


class ContactTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    contacts_list = Contact.objects.all()
    extra_context = {
        'contact_list': contacts_list,
    }
    template_name = 'catalog/contact.html'

    def post(self, request):
        """Вывод сообщения из формы обратной связи"""
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(f'You have a message from {name}({email}): {message}')
        return render(request, 'catalog/contact.html', context=self.extra_context)


class ProductListView(LoginRequiredMixin, ListView):
    """Контроллер страницы товаров"""
    model = Product
    paginate_by = 6


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления товара от пользователя"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        """Добавление автора к товару"""
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения отдельного товара"""
    model = Product


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер страницы редактирования товара"""
    model = Product

    def get_success_url(self):
        return reverse_lazy('catalog:products')

    def test_func(self):
        custom_perms = (
            'catalog.set_is_published',
            'catalog.set_category',
            'catalog.set_description'
        )
        if self.request.user == self.get_object().author or self.request.user.is_superuser is True:
            return True
        elif self.request.user.groups.filter(name='moderators').exists() and self.request.user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()

    def get_form_class(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return ModeratorProductForm
        return ProductForm

    def get_context_data(self, **kwargs):
        """Добавление формсета 'Версия' к товару"""
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = FormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = FormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Сохранение данных из формсета"""
        formset = self.get_context_data()['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
                else:
                    return self.form_invalid(form)

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        if self.request.user == self.get_object().author or self.request.user.is_superuser is True:
            return True
        return self.handle_no_permission()

