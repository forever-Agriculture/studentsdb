# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    """Student Model"""

    class Meta(object):
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенти"

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я")

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище")

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По - батькові",
        default='')

    student_group = models.ForeignKey('Group',
        verbose_name=u'Група',
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    birthday = models.DateField(
        blank=False,
        verbose_name=u"Дата народження",
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null = True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Квиток")

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class Group(models.Model):
    """Group Model"""

    class Meta(object):
        verbose_name = u"Група"
        verbose_name_plural = u"Групи"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва")

    leader = models.OneToOneField('Student',
        blank=True,
        null=True,
        verbose_name=u"Староста",
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        if self.leader:
            return u'{} {} {}'.format(self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u'{}'.format(self.title)



class Journal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name = u"Журнал"
        verbose_name_plural = u"Журнали"

    student_hookey = models.OneToOneField('Student',
        blank=True,
        null=True,
        verbose_name=u"Прогуляка",
        on_delete=models.SET_NULL)

    def __unicode__(self):
        if self.student_hookey:
            return u'{} {}'.format(self.student_hookey.first_name, self.student_hookey.last_name)
        else:
            return