from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ModeratorProductForm, ProductForm, VersionForm
from catalog.models import Contact, Product, Version, Category
from catalog.service import check_user


class HomeListView(LoginRequiredMixin, ListView):
    """Контроллер домашней страницы"""
    model = Product
    template_name = 'catalog/home_list.html'

    def get_queryset(self):
        """Отображение только 5 последних добавленных товаров"""
        return super().get_queryset().order_by('-pk')[:5]


class ContactTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    template_name = 'catalog/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_list'] = Contact.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """Вывод сообщения из формы обратной связи"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have a message from {name}({email}): {message}')
        return self.render_to_response(self.get_context_data(**kwargs))


class ProductListView(LoginRequiredMixin, ListView):
    """Контроллер страницы товаров"""
    model = Product
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().order_by('pk')
        category_id = self.request.GET.get('category', '').strip()
        query = self.request.GET.get('q', '').strip()

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '').strip()
        context['search_query'] = self.request.GET.get('q', '').strip()

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_string'] = query_params.urlencode()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления товара от пользователя"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        """Добавление автора к товару"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения отдельного товара"""
    model = Product


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер страницы редактирования товара"""
    model = Product
    success_url = reverse_lazy('catalog:products')

    def is_moderator(self):
        return self.request.user.groups.filter(name='moderators').exists()

    def test_func(self):
        user = self.request.user
        author = self.get_object().author
        if check_user(user, author):
            return True
        return self.handle_no_permission()

    def get_form_class(self):
        if self.is_moderator():
            return ModeratorProductForm
        return ProductForm

    def _build_formset(self):
        if self.is_moderator():
            return None
        formset_class = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            return formset_class(self.request.POST, instance=self.object)
        return formset_class(instance=self.object)

    def get_context_data(self, **kwargs):
        """Добавление формсета 'Версия' к товару"""
        context_data = super().get_context_data(**kwargs)
        context_data['formset'] = self._build_formset()
        return context_data

    def form_valid(self, form):
        """Сохранение товара и формсета версий"""
        if self.is_moderator():
            return super().form_valid(form)

        self.object = form.save(commit=False)
        formset_class = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        formset = formset_class(self.request.POST, instance=self.object)

        if not formset.is_valid():
            context = self.get_context_data(form=form)
            context['formset'] = formset
            return self.render_to_response(context)

        with transaction.atomic():
            self.object.author = self.object.author or self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления товара"""
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.author or self.request.user.is_superuser:
            return True
        return self.handle_no_permission()