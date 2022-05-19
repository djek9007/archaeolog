from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from employees.models import MonografiEmployer, Employer, Department

class DepartmentAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget(), required=False)

@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    """Статичные страницы"""
    list_display = ('tree_actions', 'indented_title', 'slug',)
    list_display_links = ('indented_title',)
    list_editable = ('slug',)
    MPTT_ADMIN_LEVEL_INDENT = 20
    # list_filter = ("published", )
    # search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}
    fields = ('parent', 'name', 'slug', 'description', 'published',)

    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    form = DepartmentAdminForm

class MonografiEmployerAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание монографии", widget=CKEditorUploadingWidget(), required=False)

@admin.register(MonografiEmployer)
class MonografiEmployerAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer','published', )
    list_filter = ('employer', 'published',)
    form = MonografiEmployerAdminForm

class EmployerAdminForm(forms.ModelForm):
    """Виджет редактора ckeditor"""
    profile = forms.CharField(label="Профиль сотрудника", widget=CKEditorUploadingWidget(), required=False)
    publication = forms.CharField(label="Основные публикации сотрудника", widget=CKEditorUploadingWidget(), required=False)
    projects = forms.CharField(label="Проекты сотрудника", widget=CKEditorUploadingWidget(), required=False)


    class Meta:
        model = Employer
        fields = '__all__'

class MonografiEmployerInline(admin.StackedInline):
    model = MonografiEmployer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    """Админка для сотруддника"""
    list_display = ('get_photo', 'name', 'regali', 'email', 'published', 'edit_date', 'views',)
    list_display_links = ('get_photo', 'name',)
    fields =('department','name', 'regali', 'email', 'get_photo', 'photo', 'profile', 'publication','projects','published_date','published',  )
    inlines = [MonografiEmployerInline]
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