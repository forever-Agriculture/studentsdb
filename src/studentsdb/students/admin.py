from django.contrib import admin
from .models import Student, Group, Journal

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Journal)