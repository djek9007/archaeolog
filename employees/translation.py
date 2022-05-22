# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from employees.models import Department, Employer


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Employer)
class EmployerTranslationOptions(TranslationOptions):
    fields = ('name', 'regali', 'profile', 'publication', 'projects',)

