# -*- coding: utf-8 -*-
from django import template
from datetime import datetime

from django.db.models import Count

from blog.models import Post, Tag

register = template.Library()



@register.simple_tag()
def show_news():
    """Получение новостей для главной страницы"""
    return Post.objects.filter(category=1, published=True, published_date__lte=datetime.now(),)[:7]


@register.simple_tag()
def event_show(count):
    """Получение ближайщих событий по указанному количеству"""
    return Post.objects.filter(published=True, event=True, event_published_date__gt=datetime.now())[:count]

@register.simple_tag()
def ekspedicii_show(count):
    """Получение новости из категории экспедиции по указанному количеству"""
    return Post.objects.filter(published=True, category=18)[:count]

