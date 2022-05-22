# -*- coding: utf-8 -*-
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

# Register your models here.
from modeltranslation.admin import TranslationAdmin

from library.models import LibraryEmployer, CategoryLibrary


@admin.register(CategoryLibrary)
class CategoryLibraryAdmin(TranslationAdmin):
    list_display =('name',)
    prepopulated_fields = {"slug": ("name",)}


class MonografiEmployerAdminForm(forms.ModelForm):
    description_kk = forms.CharField(label="Описание монографии на казахском", widget=CKEditorUploadingWidget(), required=False)
    description_ru = forms.CharField(label="Описание монографии на русском", widget=CKEditorUploadingWidget(), required=False)
    description_en = forms.CharField(label="Описание монографии на английском", widget=CKEditorUploadingWidget(), required=False)

@admin.register(LibraryEmployer)
class LibraryEmployerAdmin(TranslationAdmin):
    list_display = ('title', 'published', )
    list_filter = ('employer', 'published',)

    form = MonografiEmployerAdminForm