# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.utils import timezone
from dynamic_filenames import FilePattern
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from employees.models import Employer

page_file_item = FilePattern(
    filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}'
)
class CategoryLibrary(MPTTModel):
    """Класс модели категорий сетей"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("url", max_length=50, unique=True, blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    published = models.BooleanField("Отображать?", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория библиотеки"
        verbose_name_plural = "Категории библиотеки"


class LibraryEmployer(models.Model):
    """Библиотека сотрудника"""
    category = models.ForeignKey(CategoryLibrary, verbose_name='Категория библиотеки', on_delete=models.CASCADE,)
    employer = models.ManyToManyField(Employer,  verbose_name='Автор(ы)', related_name='employers')
    title = models.CharField(verbose_name='Наименование монографии', max_length=250)
    image = models.ImageField("Обложка монографии", upload_to=page_file_item, blank=True, null=True)
    description = models.TextField('Описание')
    file = models.FileField('Файл для скачивание', upload_to=page_file_item,  blank=True, null=True)
    published = models.BooleanField("Отображать?", default=True)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    class Meta:
        verbose_name = "Библиотека сотрудника"
        verbose_name_plural = "Библиотека сотрудников"

    def __str__(self):
        return self.title


class Journal(models.Model):
    title = models.CharField(verbose_name='Наименование номера журнала', max_length=250)
    image = models.ImageField("Обложка журнала", upload_to=page_file_item, blank=True, null=True)
    description = models.TextField('Описание')
    file = models.FileField('Файл для скачивание', upload_to=page_file_item, blank=True, null=True)
    link = models.CharField('Внешняя ссылка на журнал', max_length=255, blank=True, null=True)
    published = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"

    def __str__(self):
        return self.title