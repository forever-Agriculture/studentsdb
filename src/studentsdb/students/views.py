# -*- coding: utf-8 -*-

# kinda important imports
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.forms import ModelForm

from .models import Student, Group, MonthJournal
from .util import paginate

# trash imports
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from crispy_forms.helper import FormHelper
from datetime import datetime, date


# Create your views here.


    # Students

# def students_list(request):
#     students = Student.objects.all()
#
#     # try to order students list
#     order_by = request.GET.get('order_by', 'last_name')
#     if order_by in ('last_name', 'first_name', 'ticket'):
#         students = students.order_by(order_by)
#         if request.GET.get('reverse', '') == '1':
#             students = students.reverse()
#
#     # paginate students
#     paginator = Paginator(students, 5)
#     page = request.GET.get('page')
#     try:
#         students = paginator.page(page)
#     except PageNotAnInteger:
#         students = paginator.page(1)
#     except EmptyPage:
#         students = paginator.page(paginator.num_pages)
#
#     return render(request, 'students/students_list.html',
#                   {'students': students})

class StudentsListView(ListView):
    template_name = 'students/students_list.html'
    queryset = Student.objects.all()
    context_object_name = 'students_list'
    paginate_by = 5

    def get_reverse_order(self):
        order_by = self.request.GET.get('order_by', 'last_name')
        # order_by = self.queryset.order_by('order_by', 'last_name')
        if order_by in ('last_name', 'first_name', 'ticket'):
            self.queryset = self.queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                self.queryset = self.queryset.reverse()
        return order_by

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context['students_range'] = range(context["paginator"].num_pages)
        context['order_by'] = self.get_reverse_order()
        return context



# def students_add(request):
#
#     # if the form was posted
#     if request.method == "POST":
#
#         # if Add button was pressed
#         if request.POST.get('add_button') is not None:
#             # check the data
#             errors = {}
#             # validate student data will go here
#             data = {'middle_name': request.POST.get('middle_name'),
#                     'notes': request.POST.get('notes')}
#             # validate user input
#             first_name = request.POST.get('first_name', '').strip()
#             if not first_name:
#                 errors['first_name'] = u"Ім'я є обов'язковим"
#             else:
#                 data['first_name'] = first_name
#             last_name = request.POST.get('last_name', '').strip()
#             if not last_name:
#                 errors['last_name'] = u"Прізвище є обов'язковим"
#             else:
#                 data['last_name'] = last_name
#             birthday = request.POST.get('birthday', '').strip()
#             if not birthday:
#                 errors['birthday'] = u"День народження є обов'язковим"
#             else:
#                 data['birthday'] = birthday
#             ticket = request.POST.get('ticket', '').strip()
#             if not ticket:
#                 errors['ticket'] = u"Квиток є обов'язковим"
#             else:
#                 try:
#                     datetime.strptime(birthday, '%Y-%m-%d')
#                 except Exception:
#                     errors['birthday'] = u"Введіть коректний формат (1998-12-30)"
#                 else:
#                     data['birthday'] = birthday
#             student_group = request.POST.get('student_group', '').strip()
#             if not student_group:
#                 errors['student_group'] = u"Оберіть групу для студента"
#             else:
#                 groups = Group.objects.filter(pk=student_group)
#                 if len(groups) != 1:
#                     errors['student_group'] = u"Оберіть групу для студента"
#                 else:
#                     data['student_group'] = groups[0]
#             photo = request.FILES.get('photo')
#             if photo:
#                 data['photo'] = photo
#
#             if not errors:
#                 # create student object
#                 student = Student(**data)
#           #      student = Student(
#            #         first_name=request.POST['first_name'],
#             #        last_name=request.POST['last_name'],
#             #        middle_name=request.POST['middle_name'],
#              #       birthday=request.POST['birthday'],
#              #       ticket=request.POST['ticket'],
#              #       student_group=Group.objects.get(pk=request.POST['student_group']),
#              #       photo=request.FILES['photo'],
#              #   )
#                 # save it to the database
#                 student.save()
#                 # redirect user to students list
#                 return HttpResponseRedirect(
#                     u'{}?status_message=Студент успішно доданий!'.format(reverse('home'))
#                     )
#
#             else:
#             # render form with errors and previous user input
#                 return render(request, 'students/students_add.html',
#                               {'groups': Group.objects.all().order_by('title'),
#                                'errors': errors})
#
#         elif request.POST.get('cancel_button') is not None:
#             # redirect to home page on cancel button
#             return HttpResponseRedirect(
#                 u'{}?status_message=Додавання студента скасоване!'.format(reverse('home'))
#                 )
#     else:
#         # initial form render
#         return render(request, 'students/students_add.html',
#                       {'groups': Group.objects.all().order_by('title')})


class StudentCreateView(CreateView):
        queryset = Student.objects.all()
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


# class StudentUpdateForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(StudentUpdateForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper(self)
#
#         # set form tag attributes
#         self.helper.form_action = reverse('students_edit',
#                                           kwargs={'pk': kwargs['instance'].id})
#         self.helper.form_method = 'POST'
#         self.helper.form_class = 'form-horizontal'
#
#         # set form field properties
#         self.helper.help_text_inline = True
#         self.helper.html5_required = True
#         self.helper.label_class = 'col-sm-2 control-label'
#         self.helper.field_class = 'col-sm-10'


class StudentUpdateView(UpdateView):
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


    # Groups

# def groups_list(request):
#     groups = Group.objects.all()
#
#     # try to order students list
#     order_by = request.GET.get('order_by', 'title')
#     if order_by in ('leader', 'title'):
#         groups = groups.order_by(order_by)
#         if request.GET.get('reverse', '') == '1':
#             groups = groups.reverse()
#
#     # paginate groups
#     paginator = Paginator(groups, 3)
#     page = request.GET.get('page')
#     try:
#         groups = paginator.page(page)
#     except PageNotAnInteger:
#         groups = paginator.page(1)
#     except EmptyPage:
#         groups = paginator.page(paginator.num_pages)
#
#     return render(request, 'students/groups_list.html',
#                   {'groups': groups})

class GroupsListView(ListView):
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


# def groups_add(request):
#
#     # if the form was posted
#     if request.method == "POST":
#
#         # if Add button was pressed
#         if request.POST.get('add_button') is not None:
#             # check the data
#             errors = {}
#             # validate student data will go here
#             data = {'notes': request.POST.get('notes')}
#             # validate user input
#             title = request.POST.get('title', '').strip()
#             if not title:
#                 errors['title'] = u"Назва є обов'язковою"
#             else:
#                 data['title'] = title
#             leader = request.POST.get('leader', '').strip()
#             if not leader:
#                 errors['leader'] = u"Оберіть старосту групи"
#             else:
#                 students = Student.objects.filter(pk=leader)
#                 if len(students) != 1:
#                     errors['leader'] = u"Оберіть групу для студента"
#                 else:
#                     data['leader'] = students[0]
#
#             if not errors:
#                 # create student object
#                 group = Group(**data)
#           #      group = Group(
#            #         title=request.POST['title'],
#              #       ticket=request.POST['ticket'],
#              #       leader=Student.objects.get(pk=request.POST['leader']),
#              #   )
#                 # save it to the database
#                 group.save()
#                 # redirect user to students list
#                 return HttpResponseRedirect(
#                     u'{}?status_message=Групу успишно додано!'.format(reverse('groups'))
#                     )
#
#             else:
#             # render form with errors and previous user input
#                 return render(request, 'students/groups_add.html',
#                               {'students': Student.objects.all().order_by('student_group'),
#                                'errors': errors})
#
#         elif request.POST.get('cancel_button') is not None:
#             # redirect to home page on cancel button
#             return HttpResponseRedirect(
#                 u'{}?status_message=Додавання групи скасоване!'.format(reverse('groups'))
#                 )
#     else:
#         # initial form render
#         return render(request, 'students/groups_add.html',
#                       {'students': Student.objects.all().order_by('student_group')})

class GroupUpdateView(UpdateView):
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


    # Journal

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
