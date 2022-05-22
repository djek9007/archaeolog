# -*- coding: utf-8 -*-
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin

from employees.models import  Employer, Department

class DepartmentAdminForm(forms.ModelForm):
    description_kk = forms.CharField(label="Қазақша", widget=CKEditorUploadingWidget(), required=False)
    description_ru = forms.CharField(label="на русском", widget=CKEditorUploadingWidget(), required=False)
    description_en = forms.CharField(label="english", widget=CKEditorUploadingWidget(), required=False)

@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin, TranslationAdmin):
    """Статичные страницы"""
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    list_editable = ('slug',)
    MPTT_ADMIN_LEVEL_INDENT = 20
    # list_filter = ("published", )
    # search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}
    fields = ('parent', 'name', 'slug', 'description', 'published', )

    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    form = DepartmentAdminForm


class EmployerAdminForm(forms.ModelForm):
    """Виджет редактора ckeditor"""
    profile_kk = forms.CharField(label="Профиль сотрудника на казахском", widget=CKEditorUploadingWidget(), required=False)
    profile_ru = forms.CharField(label="Профиль сотрудника на русском", widget=CKEditorUploadingWidget(), required=False)
    profile_en = forms.CharField(label="Профиль сотрудника на английском", widget=CKEditorUploadingWidget(), required=False)
    publication_kk = forms.CharField(label="Основные публикации сотрудника на казахском", widget=CKEditorUploadingWidget(), required=False)
    publication_ru = forms.CharField(label="Основные публикации сотрудника на русском", widget=CKEditorUploadingWidget(), required=False)
    publication_en = forms.CharField(label="Основные публикации сотрудника на английском", widget=CKEditorUploadingWidget(), required=False)
    projects_kk = forms.CharField(label="Проекты сотрудника на казахском", widget=CKEditorUploadingWidget(), required=False)
    projects_ru = forms.CharField(label="Проекты сотрудника на русском", widget=CKEditorUploadingWidget(), required=False)
    projects_en = forms.CharField(label="Проекты сотрудника на английском", widget=CKEditorUploadingWidget(), required=False)


    class Meta:
        model = Employer
        fields = '__all__'



@admin.register(Employer)
class EmployerAdmin(TranslationAdmin):
    """Админка для сотруддника"""
    list_display = ('get_photo', 'name', 'regali', 'email', 'published', 'edit_date', 'views',)
    list_display_links = ('get_photo', 'name',)
    fields =('department','name', 'regali', 'email', 'get_photo', 'photo', 'profile', 'publication','projects','published_date','published',  'is_active',)

    form = EmployerAdminForm
    save_on_top = True
    readonly_fields = ('edit_date', 'views', 'get_photo',)
    list_filter = ('department',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра фото'