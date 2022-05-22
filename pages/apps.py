# -*- coding: utf-8 -*-
from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Страница'
    verbose_name_plural = 'Страницы'