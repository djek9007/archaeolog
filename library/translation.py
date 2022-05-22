# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


from library.models import CategoryLibrary, LibraryEmployer


@register(CategoryLibrary)
class CategoryLibraryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(LibraryEmployer)
class EmployerTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

