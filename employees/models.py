from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from sorl.thumbnail import get_thumbnail





class Department(MPTTModel):
    """Модель отделов"""
    name = models.CharField("Название", max_length=100)
    slug = models.CharField("url", max_length=50, unique=True, blank=True, null=True)
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
    regali= models.CharField(verbose_name="Регали сотрудника, должность", max_length=200)
    email= models.EmailField(verbose_name="Почта сотрудника", max_length=200)
    photo = models.ImageField('Фото сотрудника', upload_to='employers/photo/%Y/%m/%d/', blank=True, null=True)
    profile = models.TextField(_("Профиль сотрудника"), blank=True, null=True)
    publication = models.TextField(_('Список основных публикаций'), blank=True, null=True)
    projects = models.TextField(_('Проекты'), blank=True, null=True)
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
    published = models.BooleanField("Отображать?", default=True)
    views = models.PositiveIntegerField("Просмотрено", default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def get_absolute_url(self):
        return reverse('employees:employer-detail', kwargs={'pk': self.id})


class MonografiEmployer(models.Model):
    """Монографии сотрудника"""
    employer = models.ForeignKey(Employer,related_name='monografiitem', on_delete=models.CASCADE, verbose_name='Сотрудник')
    title = models.CharField(verbose_name='Наименование монографии', max_length=250)
    image = models.ImageField("Обложка монографии", upload_to="employers/monografi/%Y/%m/%d/", blank=True, null=True)
    description = models.TextField('Описание')
    file = models.FileField('Файл для скачивание', upload_to='employers/monografi/%Y/%m/%d/',  blank=True, null=True)
    published = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Монография сотрудника"
        verbose_name_plural = "Монографии сотрудников"

    def __str__(self):
        return self.title