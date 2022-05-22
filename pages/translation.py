# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from menu.models import Menu
from pages.models import Pages


@register(Pages)
class PagesTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


