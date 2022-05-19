from django.urls import path
from . import views

app_name='employees'

urlpatterns = [
    path('', views.EmployeesListView.as_view(), name='employer-list'),
    path('<int:pk>', views.EmployeerDetailView.as_view(), name='employer-detail'),
]