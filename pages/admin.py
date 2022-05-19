from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.text import slugify

from .models import Pages, FileItem, PhotoItem


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



class PagesAdminForm(forms.ModelForm):
    """Виджет редактора ckeditor"""
    text = forms.CharField(label="Контент страницы", widget=CKEditorUploadingWidget())

    class Meta:
        model = Pages
        fields = '__all__'


class FileItemInline(admin.TabularInline):
    model = FileItem


class PhotoItemInline(admin.TabularInline):
    model = PhotoItem

@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    """Статичные страницы"""
    list_display = ("title", "published", 'slug', "id")
    list_editable = ("published", )
    list_filter = ("published", )
    search_fields = ("title",)
    inlines = [PhotoItemInline, FileItemInline, ]
    prepopulated_fields = {"slug": ("title", )}
    form = PagesAdminForm
    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)

    # def save_model(self, request, obj, form, change):
    #     # don't overwrite manually set slug
    #     if form.cleaned_data['slug']:
    #         obj.slug = 'page' + '/' + form.cleaned_data['slug']
    #     obj.save()