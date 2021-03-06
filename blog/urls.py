# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [

    # path('laboratorii/', views.LaboratoriiView.as_view(), name='laboratorii'),
    path('page-<slug:slug>/', views.PageView.as_view(), name='page'),
    path('<slug:category_slug>/', views.PostList.as_view(), name='category_post'),

    path('<slug:category_slug>/<slug:slug>/', views.PostDetail.as_view(), name='detail_post'),


    path('', views.Home.as_view(), name='home'),

]
