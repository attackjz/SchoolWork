# coding=utf-8

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
import datetime
from polls.models import *
from django.views import generic
# Create your views here.


def index(request):
    templates = 'home/index.html'
    # templates = 'role/teacher_regist.html'

    # l = ['a', 'b', 'c', 'd', 'e', ]
    #
    # d = {
    #     'A': 'hello',
    #     'B': 'world',
    # }
    context = {
        # 'msg': 'hello',
        # 'time': datetime.datetime.now(),
        # 'list': l,
        # 'dict': d,
    }

    return render(
        request,
        templates,
        context
    )


def TeacherRegist(request):

    template = 'role/teacher_regist.html'
    print request
    # template = 'home/index.html'
    context = {

    }

    return render(
        request,
        template,
        context,
    )


def StudentRegist(request):

    template = 'role/teacher_regist.html'

    return render(
        request,
        template,
    )
