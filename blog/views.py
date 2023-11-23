from pytils.translit import slugify
from django.core.mail import send_mail

from blog.models import Blog
from config.settings import EMAIL_HOST_USER

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ArticleListView(LoginRequiredMixin, ListView):
    """Контроллер отображения страницы статей"""
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """Отображение только опубликованных статей"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения отдельной статьи"""
    model = Blog

    def get_object(self, queryset=None):
        """Реализация счетчика просмотров и отправка письма на почту при достижении 100 просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 100:
            send_mail(
                'Вы популярны!!!!',
                'Вы набрали 100 просмотров',
                EMAIL_HOST_USER,
                ['ya.savchik2000@mail.ru']
            )
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published')
    success_url = reverse_lazy('blog:articles')

    def form_valid(self, form):
        """Генерация slug к статье"""
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published',)
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        """Обновление slug"""
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на статью"""
        return reverse('blog:view', args=[self.kwargs.get('slug')])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления статьи"""
    permission_required = 'blog.delete_blog'
    model = Blog
    success_url = reverse_lazy('blog:articles')
