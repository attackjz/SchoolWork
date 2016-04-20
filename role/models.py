# coding=utf-8

from __future__ import unicode_literals
from django.db import models

from django.utils import timezone
from django.contrib.auth.models import *

import time, random, re
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


#  科目
class Subject(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, unique=True)
    teacher = models.ForeignKey(Teacher, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '科目'
        verbose_name_plural = '科目'


# 班级
class StuToSub(models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)

    class Meta:
        verbose_name = '学生科目关系'
        verbose_name_plural = '学生科目关系'


# 重命名文件名
def resource_file_path(instance, filename):
    # file_time = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time()))
    ft = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    # format = re.search("\.\w+$",  filename)
    format = re.findall("\.\w+$", filename)
    filename = str(ft) + instance.name + format[0]
    return '/'.join(['courseware', 'resource', time.strftime('%m%d', time.localtime(time.time())), filename])


# 课件
class Courseware(models.Model):
    # number = models.IntegerField(unique=True, null=True, )
    name = models.CharField(max_length=128)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    subject = models.ManyToManyField(Subject)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to=resource_file_path)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'role_courseware'
        app_label = 'role'
        verbose_name = '课件'
        verbose_name_plural = '课件'
