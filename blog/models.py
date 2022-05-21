from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    """Класс модели категорий сетей"""
    name = models.CharField("Название", max_length=100)
    slug = models.CharField("url", max_length=50, unique=True, blank=True, null=True)
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
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_post', kwargs={'category_slug': self.slug})


def post_photo_path(instance, filename):
    return 'posts/post_{0}/{1}'.format(instance.pk, filename)

class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Название тега', max_length=100, unique=True)
    slug = models.SlugField('url', max_length=50, unique=True)
    published = models.BooleanField("отображать?", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Post(models.Model):
    """Класс модели поста"""
    title = models.CharField("Заголовок", max_length=500)
    slug = models.SlugField("url", max_length=50, unique=True)
    text = models.TextField("Содержание")
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
    image = models.ImageField("Главная фотография", upload_to=post_photo_path)
    category = TreeForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    published = models.BooleanField("Опубликовать?", default=True)
    event = models.BooleanField('Показать в разделе ближайщее событие', default=False)
    event_published_date = models.DateTimeField(
        "Дата событие",
        default=timezone.now,
        blank=True,
        null=True
    )
    video = models.CharField(_('Ссылка на видео'), max_length=255, blank=True, null=True)
    views = models.PositiveIntegerField("Просмотрено", default=0)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(Post, self).save(*args, **kwargs)
            self.image = saved_image

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail_post', kwargs={'category_slug': self.category.slug,'slug': self.slug})

def post_photo_item(instance, filename):

    return 'posts/post_item_{0}/{1}'.format(instance.pk, filename)

class PhotoItem(models.Model):
    image = models.ImageField(upload_to='posts/item_photo/%Y/%m/%d/', verbose_name='Галерея', blank=True, null=True, unique=True)
    photo = models.ForeignKey(Post, related_name='photoitems', on_delete=models.CASCADE)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    def __str__(self):
        return str(self.photo.id)

    class Meta:
        verbose_name = "Галерея постов"
        verbose_name_plural = "Галерея постов"



def post_file_item(filename):

    return 'files/post/%Y/%m/%d/{0}/'.format(filename)


class FileItem(models.Model):
    file = models.FileField(upload_to=post_file_item, verbose_name='Файлы', blank=True, null=True, unique=True)
    post = models.ForeignKey(Post, related_name='fileitems', on_delete=models.CASCADE)
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)
    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = "Файл для прикрепление"
        verbose_name_plural = "Файлы для прикрепление"
