from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:category_slug>/', views.PostList.as_view(), name='category_post'),
    path('<slug:category_slug>/<slug:slug>/', views.PostDetail.as_view(), name='detail_post'),
]