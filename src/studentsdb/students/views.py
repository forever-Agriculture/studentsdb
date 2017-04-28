# -*- coding: utf-8 -*-

# core imports
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.forms import ModelForm

# other imports
from calendar import monthrange, weekday, day_abbr
from crispy_forms.helper import FormHelper

# app imports
from .models import Student, Group, MonthJournal
from .util import paginate


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


class StudentCreateView(CreateView):
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

    def get_reverse_order(self):
        order_by = self.request.GET.get('order_by', 'title')
        if order_by in ('leader', 'title'):
            self.queryset = self.queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                self.queryset = self.queryset.reverse()
        return order_by

    def get_context_data(self, **kwargs):
        context = super(GroupsListView, self).get_context_data(**kwargs)
        context['groups_range'] = range(context["paginator"].num_pages)
        context['order_by'] = self.get_reverse_order()
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


class GroupDeleteView(DeleteView):
    model = Group
    fields = '__all__'
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return u'{}?status_message=Група успішно видалена!'.format(reverse('groups'))


# Journal Views
class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        context['cur_month'] = month.strftime('%Y-%m-%d')

        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
                                    'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
                                   for d in range(1, number_of_days + 1)]

        queryset = Student.objects.order_by('last_name')

        update_url = reverse('journal')

        students = []
        for student in queryset:
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            days = []
            for day in range(1, number_of_days + 1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day{}'.format(day),
                                                   False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            students.append({
                'fullname': u'{} {}'.format(student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

            context = paginate(students, 10, self.request, context, var_name='students')

            return context
