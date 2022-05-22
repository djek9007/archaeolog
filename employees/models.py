# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.utils import timezone
from dynamic_filenames import FilePattern
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from sorl.thumbnail import get_thumbnail

page_file_item = FilePattern(
    filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}'
)

class Department(MPTTModel):
    """Модель отделов"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("url", max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(verbose_name='Описание отдела')
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительский отдел",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
    )
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,

    )
    published = models.BooleanField("Отображать?", default=True)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"


class Employer(models.Model):
    """Модель сотрудника"""
    department = TreeForeignKey(
        Department,
        verbose_name="Отдел",
        on_delete=models.CASCADE,
    )
    name= models.CharField(verbose_name="ФИО сотрудника", max_length=200)
    regali= models.CharField(verbose_name="Регали сотрудника, должность", max_length=255)
    email= models.EmailField(verbose_name="Почта сотрудника", max_length=100)
    photo = models.ImageField('Фото сотрудника', upload_to=page_file_item, blank=True, null=True)
    profile = models.TextField(_("Профиль сотрудника"), blank=True, null=True)
    publication = models.TextField(_('Список основных публикаций'), blank=True, null=True)
    projects = models.TextField(_('Проекты'), blank=True, null=True)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    is_active = models.BooleanField(_('Действующий?'), default=True)
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
    published = models.BooleanField("Отображать?", default=True)
    views = models.PositiveIntegerField("Просмотрено", default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def get_absolute_url(self):
        return reverse('employees:employer-detail', kwargs={'pk': self.id})


