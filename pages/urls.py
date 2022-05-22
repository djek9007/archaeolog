# -*- coding: utf-8 -*-
from django.urls import path

from pages import views

app_name = 'pages'

urlpatterns = [
    path('', views.PageView.as_view(), name='page-detail'),
]
