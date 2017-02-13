# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

    # Students
def students_list(request):

    students = (
        {'id': 1,
         'first_name': u'Надія',
         'last_name': u'Гілюк',
         'ticket': 21,
         'image': '1.png'},
        {'id': 2,
         'first_name': u'Роман',
         'last_name': u'Блажкевич',
         'ticket': 6,
         'image': '1.png'},
        {'id': 3,
         'first_name': u'Платон',
         'last_name': u'Гатило',
         'ticket': 26,
         'image': '1.png'},
    )

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
        {'id': 1,
         'name': u'ІПС-3',
         'leader': {'id': 1, 'name': u'Новий Василь'}},
    )

    return render(request, 'students/groups_list.html',
                  {"groups": groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

