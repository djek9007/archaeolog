from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from blog.models import Category, Post, PhotoItem, Tag, FileItem


class ActionPublish(admin.ModelAdmin):
    """Action для публикации и снятия с публикации"""

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        rows_updated = queryset.update(published=False)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        """Опубликовать"""
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Статичные страницы"""
    list_display = ('tree_actions', 'indented_title',)
    list_display_links = ('indented_title',)
    MPTT_ADMIN_LEVEL_INDENT = 20
    list_filter = ("published", )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}

    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)

class PostAdminForm(forms.ModelForm):
    """Виджет редактора ckeditor"""
    text = forms.CharField(required=False, label="Контент страницы", widget=CKEditorUploadingWidget())
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label='Категория')

    class Meta:
        model = Post
        fields = '__all__'

class PhotoItemInline(admin.TabularInline):
    model = PhotoItem


class FileItemInline(admin.TabularInline):
    model = FileItem


@admin.register(Post)
class PostAdmin(ActionPublish):
    """Статичные страницы"""
    list_display = ('get_image', "title", "published",'slug', "id", 'category', )
    list_display_links = ['get_image', 'title',]
    fields =('category', 'title', 'slug', 'text', 'image',  'published', 'published_date', 'event', 'event_published_date', 'tags',)
    # list_editable = ("published",)
    list_filter = ("published",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title", )}
    form = PostAdminForm
    actions = ['unpublish', 'publish']
    inlines = [PhotoItemInline, FileItemInline,]
    list_per_page = 50 #разделение записи
    readonly_fields = ('edit_date', 'views',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50">')
        else:
            return '-'

    get_image.short_description = 'Миниатюра фото'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'published',)
    prepopulated_fields = {'slug': ('name',)}