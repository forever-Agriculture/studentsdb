# -*- coding: utf-8 -*-

# core imports
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# app imports
from .models import Student, Group


# Student Views
class StudentsListView(ListView):
    """..."""
    template_name = 'students/students_list.html'
    model = Student
    context_object_name = 'students_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super(StudentsListView, self).get_queryset()
        order_by = self.request.GET.get('order_by', 'last_name')
        if order_by in ('last_name', 'first_name', 'ticket'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context['students_range'] = range(context["paginator"].num_pages)
        return context


class StudentCreateView(SuccessMessageMixin, CreateView):
    """..."""
    model = Student
    template_name = 'students/students_add.html'
    fields = '__all__'

    def get_success_url(self):
        return u'{}?status_message=Студент доданий!'.format(reverse('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                u'{}?status_message=Додавання студента скасоване!'.format(reverse('home'))
            )
        else:
            return super(StudentCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class StudentUpdateView(UpdateView):
    """..."""
    model = Student
    fields = '__all__'
    template_name = 'students/students_edit.html'

    def get_success_url(self):
        return u'{}?status_message=Студент відредагований!'.format(reverse('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                u'{}?status_message=Редагування студента скасоване!'.format(reverse('home'))
                )
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class StudentDeleteView(DeleteView):
    model = Student
    fields = '__all__'
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'{}?status_message=Студент успішно видалений!'.format(reverse('home'))


# Group Views
class GroupsListView(ListView):
    """..."""
    queryset = Group.objects.all()
    template_name = 'students/groups_list.html'
    context_object_name = 'groups_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(GroupsListView, self).get_queryset()
        order_by = self.request.GET.get('order_by', 'title')
        if order_by in ('leader', 'title'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupsListView, self).get_context_data(**kwargs)
        context['groups_range'] = range(context["paginator"].num_pages)
        return context


class GroupCreateView(CreateView):
    """..."""
    queryset = Group.objects.all()
    template_name = 'students/groups_add.html'
    fields = '__all__'

    def get_success_url(self):
        return u'{}?status_message=Група додана!'.format(reverse('groups'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                u'{}?status_message=Додавання групи скасоване!'.format(reverse('groups'))
            )
        else:
            return super(GroupCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context


class GroupUpdateView(UpdateView):
    """..."""
    model = Group
    fields = '__all__'
    template_name = 'students/groups_edit.html'

    def get_success_url(self):
        return u'{}?status_message=Групу успішно відредаговано!'.format(reverse('groups'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'{}?status_message=Редагування групи скасоване!'.format(reverse('groups'))
                )
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context


class GroupDeleteView(DeleteView):
    """..."""
    model = Group
    fields = '__all__'
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return u'{}?status_message=Група успішно видалена!'.format(reverse('groups'))
