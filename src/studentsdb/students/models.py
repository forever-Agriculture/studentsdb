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


class MonthJournal(models.Model):
    """Student Monthly Journal"""

    class Meta(object):
        verbose_name = u"Місячний журнал"
        verbose_name_plural = u"Місячні журнали"

    student = models.ForeignKey('Student',
    verbose_name=u'Студент',
    blank=False,
    unique_for_month='date')

    date = models.DateField(
    verbose_name=u'Дата',
    blank=False)

    present_day1 = models.BooleanField(default=False)
    present_day2 = models.BooleanField(default=False)
    present_day3 = models.BooleanField(default=False)
    present_day4 = models.BooleanField(default=False)
    present_day5 = models.BooleanField(default=False)
    present_day6 = models.BooleanField(default=False)
    present_day7 = models.BooleanField(default=False)
    present_day8 = models.BooleanField(default=False)
    present_day9 = models.BooleanField(default=False)
    present_day10 = models.BooleanField(default=False)
    present_day11 = models.BooleanField(default=False)
    present_day12 = models.BooleanField(default=False)
    present_day13 = models.BooleanField(default=False)
    present_day14 = models.BooleanField(default=False)
    present_day15 = models.BooleanField(default=False)
    present_day16 = models.BooleanField(default=False)
    present_day17 = models.BooleanField(default=False)
    present_day18 = models.BooleanField(default=False)
    present_day19 = models.BooleanField(default=False)
    present_day20 = models.BooleanField(default=False)
    present_day21 = models.BooleanField(default=False)
    present_day22 = models.BooleanField(default=False)
    present_day23 = models.BooleanField(default=False)
    present_day24 = models.BooleanField(default=False)
    present_day25 = models.BooleanField(default=False)
    present_day26 = models.BooleanField(default=False)
    present_day27 = models.BooleanField(default=False)
    present_day28 = models.BooleanField(default=False)
    present_day29 = models.BooleanField(default=False)
    present_day39 = models.BooleanField(default=False)
    present_day31 = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{} {} {}'.format(self.student.last_name, self.date.month, self.date.year)
