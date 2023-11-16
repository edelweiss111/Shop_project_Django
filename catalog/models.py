from django.conf import settings
from django.db import models
import psycopg2
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Product(models.Model):
    """Модель таблицы - товары"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Превью')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_modified = models.DateField(auto_now=True, verbose_name='Дата изменения')
    price = models.IntegerField(verbose_name='Цена', default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                               verbose_name='Кем создан')

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    """Модель таблицы - категории"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
    """Модель таблицы - контакты"""
    name = models.CharField(max_length=150, verbose_name='Имя')
    email = models.EmailField(max_length=150, verbose_name='Почта')
    post = models.CharField(max_length=150, verbose_name='Должность')

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Version(models.Model):
    """Модель таблицы - версия"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    number = models.FloatField(verbose_name='Номер версии')

    is_active = models.BooleanField(default=False, verbose_name='Активна')

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


@receiver(post_save, sender=Version)
def set_active_version(sender, instance, **kwargs):
    """При установке флага версии в режим 'активна' версии, которые были активны до этого перестают быть активными"""
    if instance.is_active:
        Version.objects.filter(product=instance.product).exclude(pk=instance.pk).update(is_active=False)
