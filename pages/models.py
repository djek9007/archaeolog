# -*- coding: utf-8 -*-
import os

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.
from dynamic_filenames import FilePattern


class Pages(models.Model):
    """Страницы"""
    title = models.CharField(_("Заголовок"), max_length=250)
    slug = models.SlugField("ссылка", max_length=50, unique=True)
    image = models.ImageField("фотография", upload_to="pages/", blank=True, null=True)
    text = models.TextField(_("Текст"), blank=True, null=True)
    edit_date = models.DateTimeField(
        _("Дата редактирования"),
        auto_now=True,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(_("Дата публикации"), blank=True, null=True, default=timezone.now,)
    published = models.BooleanField(_("Опубликовать?"), default=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


# def page_file_item(instance, filename):
#     fname, dot, extension = filename.rpartition('.')
#     slug = slugify(instance.file)
#     return '%s.%s' % (slug, extension)

# def page_file_item(self, filename):
#     name, ext = os.path.splitext(filename)
#     return os.path.join('page/file/%Y/%m/%d/', str(self.page.pk), slugify(name) + ext)

# def page_file_item(instance, filename):
#     return ''.join("page/file/%Y/%m/%d/{0}".format(instance, slugify(filename)))

page_file_item = FilePattern(
    filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}'
)

class FileItem(models.Model):
    file = models.FileField(upload_to=page_file_item, verbose_name='Файлы', blank=True, null=True)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    page = models.ForeignKey(Pages, related_name='fileitems', on_delete=models.CASCADE)
    #
    # def __unicode__(self):
    #     return 'uni: %s' % self.file.encode('utf-8')

    class Meta:
        verbose_name = "Файл для прикрепление"
        verbose_name_plural = "Файлы для прикрепление"


# def page_photo_item(instance, filename):
#     return ''.join("page/item_photo/{0}/%Y/%m/%d/".format(instance.pk, slugify(filename)))



class PhotoItem(models.Model):
    image = models.ImageField(upload_to=page_file_item, verbose_name='Галерея', blank=True, null=True, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    photo = models.ForeignKey(Pages, related_name='photoitems', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.photo.id)

    class Meta:
        verbose_name = "Галерея постов"
        verbose_name_plural = "Галерея постов"
