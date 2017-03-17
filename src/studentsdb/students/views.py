# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from .models import Student, Group, Journal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

    # Students

def students_list(request):
    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', 'last_name')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html',
                  {'students': students})


def students_add(request):

    # if the form was posted
    if request.method == "POST":

        # if Add button was pressed
        if request.POST.get('add_button') is not None:
            # check the data
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"День народження є обов'язковим"
            else:
                data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Квиток є обов'язковим"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат (1998-12-30)"
                else:
                    data['birthday'] = birthday
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть групу для студента"
                else:
                    data['student_group'] = groups[0]
            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            if not errors:
                # create student object
                student = Student(**data)
          #      student = Student(
           #         first_name=request.POST['first_name'],
            #        last_name=request.POST['last_name'],
            #        middle_name=request.POST['middle_name'],
             #       birthday=request.POST['birthday'],
             #       ticket=request.POST['ticket'],
             #       student_group=Group.objects.get(pk=request.POST['student_group']),
             #       photo=request.FILES['photo'],
             #   )
                # save it to the database
                student.save()
                # redirect user to students list
                return HttpResponseRedirect(u'%s?status_message=Студент успішно доданий!' %
                                            reverse('home'))
            else:
            # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif  request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасоване!' %
                                            reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title')})


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

    # Groups

def groups_list(request):
    groups = Group.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', 'title')
    if order_by in ('leader', 'title'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html',
                  {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

    # Journal

def journal_list(request):
    hookeys = Journal.objects.all()

    return render(request, 'students/journal_list.html',
                  {'hookeys': hookeys})
