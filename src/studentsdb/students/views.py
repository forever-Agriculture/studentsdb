# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

# Create your views here.

    # Students

def students_list(request):
    students = Student.objects.all()
    return render(request, 'students/students_list.html',
                  {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

    # Groups

def groups_list(request):

    groups = (
        {'id': 1,
         'name': u'ІПС-2',
         'leader': {'id': 1, 'name': u'Арістотель Хтосько'}},
        {'id': 2,
         'name': u'ІПС-3',
         'leader': {'id': 2, 'name': u'Новий Василь'}},
    )

    return render(request, 'students/groups_list.html',
                  {"groups": groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

    # Journal

def journal_list(request):

    hookeys = (
        {'id': 1,
         'full_name': u'Гілюк Надія'},
        {'id': 2,
         'full_name': u'Блажкевич Роман'},
        {'id': 3,
         'full_name': u'Гатило Платон'},
    )

    return render(request, 'students/journal_list.html',
                  {'hookeys': hookeys})
