# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from employees.models import Employer
from library.models import LibraryEmployer


class EmployeesListView(ListView):
    model = Employer
    template_name = 'employees/employers_list.html'
    context_object_name = 'employees'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(EmployeesListView, self).get_context_data(**kwargs)
        employess = self.get_queryset().filter(published=True).order_by('name')
        page = self.request.GET.get('page')
        paginator = Paginator(employess, self.paginate_by)
        try:
            employess = paginator.page(page)
        except PageNotAnInteger:
            employess = paginator.page(1)
        except EmptyPage:
            employess = paginator.page(paginator.num_pages)
        context['employess'] = employess
        return context

class EmployeerDetailView(View):
    def get(self, request, pk):
        employer = get_object_or_404(Employer, pk=pk)
        monografi = LibraryEmployer.objects.filter(employer=employer)
        context = {
            'employer': employer,
            'monografi': monografi
        }
        return render(request, 'employees/employers_detail.html', context)
