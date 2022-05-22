# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from blog.models import Category, Post


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

