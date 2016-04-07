# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.contrib import auth
from django.views import generic
from django import forms

import models


def index(request):
    # templates = 'role/teacher_regist.html'

    context = {
        'msg ' : 'sdawdaw',
    }

    return render(
        request,
        # templates,
        context,
    )


class UploadForm(forms.Form):
    name = forms.CharField(max_length=32)
    courseware = forms.FileField('/static/courseware/')


def upload(request):
    if request.method == 'POST':

        uf = UploadForm(request.POST, request.FILES)
        if uf.is_valid():
            # name = uf.name
            # courseware = uf.courseware
            return HttpResponse("upload success!")
        # name = uf.name
        # return HttpResponse(name)

        # else:
        #     return HttpResponse("error !")

    else:
        uf = UploadForm()

    return render(request,
                  'role/upload.html',
                  {'uf': uf})


class Regist(generic.View):

    template_name = 'role/teacher_regist.html'

    def get(self, request):
        context = {

        }

        return render(
            request,
            self.template_name,
            context,
        )


def register(request):

    print request.POST

    post_data = request.POST

    username = post_data['username']
    pw = post_data['password']
    pw_cm = post_data['pw_confirm']
    groups = post_data['groups']

    print "username is %s , pw is %s groups is %s" % (username, pw, groups)

    if username == '':
        return HttpResponse("null username")

    if pw != pw_cm:
        return HttpResponse("pass error")

    check_user = models.User.objects.filter(username=username)

    if check_user:
        return HttpResponse("username is already in sign")

    user = models.User.objects.create_user(username, "temp@temp.com", pw)
    user.save()

    g = models.Group.objects.get(name=groups)
    user.groups.add(g)
    if "Student" == groups:
        stu = models.Student.objects
        s = models.Student(user=user)
        s.save()

    if "Teacher" == groups:
        stu = models.Teacher.objects
        s = models.Teacher(user=user)
        s.save()

    return HttpResponse('regist success')
    # return render(
    #     request,
    #
    # )

# Create your views here.
