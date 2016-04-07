# coding=utf-8

from __future__ import unicode_literals
from django.db import models

from django.utils import timezone
from django.contrib.auth.models import *

import datetime
from home.models import *

# Create your models here.


def show_name(user):
    name = user.first_name + user.last_name
    if name:
        return name
    else:
        return user.username


class Teacher(models.Model):
    number = models.IntegerField(unique=True, null=True, blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return show_name(self.user)


class Student(models.Model):
    number = models.IntegerField(unique=True, null=True, blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return show_name(self.user)


# 班级
class Team(models.Model):
    number = models.IntegerField()
    grade = models.IntegerField()
    teacher = models.ManyToManyField(Teacher, related_name='teacher')
    student = models.ManyToManyField(Student, related_name='student')

    def __unicode__(self):
        return str(self.grade) + '-' + str(self.number)


# 课程
class Subject(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, unique=True)
    teacher = models.ManyToManyField(Teacher)
    team = models.ManyToManyField(Team)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'



# 课件
class Courseware(models.Model):
    number = models.IntegerField(unique=True, auto_created=True)
    name = models.CharField(max_length=64)
    pub_datetime = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField('/static/courseware/')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'role_courseware'
        app_label = 'role'
        verbose_name = '课件'
        verbose_name_plural = '课件'
