# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models import Student, Group, MonthJournal


class StudentFormAdmin(ModelForm):
    """..."""
    def clean_student_group(self):
        """Check if a student is leader in any group.
           if it is, make sure it's the same selected group.
           get group where current student is a leader
        """
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    """..."""
    form = StudentFormAdmin

    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    search_fields = ['last_name', 'first_name', 'ticket', 'notes']
    list_per_page = 5

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupAdmin(admin.ModelAdmin):
    """..."""
    search_fields = ['title', 'leader__first_name', 'leader__first_name', 'notes']
    list_per_page = 5


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)
