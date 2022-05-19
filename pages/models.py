from django.db import models
from django.template.defaultfilters import slugify

from django.utils.translation import gettext_lazy as _


# Create your models here.
class Pages(models.Model):
    """Страницы"""
    title = models.CharField(_("Заголовок"), max_length=250)
    slug = models.CharField("ссылка", max_length=50, unique=True)
    image = models.ImageField("фотография", upload_to="pages/", blank=True, null=True)
    text = models.TextField(_("Текст"), blank=True, null=True)
    edit_date = models.DateTimeField(
        _("Дата редактирования"),
        auto_now=True,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(_("Дата публикации"), blank=True, null=True)
    published = models.BooleanField(_("Опубликовать?"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"




class FileItem(models.Model):
    file = models.FileField(upload_to='files/page/%Y/%m/%d/', verbose_name='Файлы', blank=True, null=True, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    page = models.ForeignKey(Pages, related_name='fileitems', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = "Файл для прикрепление"
        verbose_name_plural = "Файлы для прикрепление"


def page_photo_item(instance, filename):
    return 'page/item_photo/{0}/%Y/%m/%d/'.format(instance.pk, filename)


class PhotoItem(models.Model):
    image = models.ImageField(upload_to=page_photo_item, verbose_name='Галерея', blank=True, null=True, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    photo = models.ForeignKey(Pages, related_name='photoitems', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.photo.id)

    class Meta:
        verbose_name = "Галерея постов"
        verbose_name_plural = "Галерея постов"
