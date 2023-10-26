from django.db import models
import psycopg2
from config.settings import DATABASES
from django.db import connection

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
