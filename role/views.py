# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.contrib.auth import models
from django.views import generic
from django import forms
from wsgiref.util import FileWrapper # 引用下载


from role.models import *

import models
import re
import time
import mimetypes # 下载

def index(request):
    # templates = 'role/teacher_regist.html'

    if request.user.is_superuser:
        user_type = 'super'
        return HttpResponseRedirect('/admin')

    else:
        user_type = Group.objects.get(user=request.user.id)
        print user_type
    name = request.user.get_full_name()
    sub_list = {}

    if 'Student' == user_type.name:
        student = Student.objects.get(user=request.user.id)
        subject_list = StuToSub.objects.filter(student=student.id)
        print subject_list.values()
        for l in subject_list.values():
            id = l['subject_id']
            s = Subject.objects.get(id=id)
            print s
            sub_list[str(id)] = s.name
        print sub_list
        name = student.__unicode__()
    elif 'Teacher' == user_type.name:
        teacher = Teacher.objects.get(user=request.user.id)
        subject_list = Subject.objects.filter(teacher=teacher)
        name = teacher.__unicode__()
        for p in subject_list:
            sub_list[p.id] = p.name

    print sub_list

    # if 'clicked' in request.GET and request.GET['clicked']:
    #     click_id = request.GET['clicked']
    #     courseware = Courseware.objects.filter(subject=click_id)
    #     courseware_list = {}
    #     for i in courseware:
    #         print i
    #         courseware_list[str(i.id)] = i.name
    #
    #     print courseware_list

    context = {
        'page_type': 'home',
        'msg ': 'sdawdaw',
        'subject_list': sub_list,
        # 'courseware_list': courseware_list,
        'user_type': user_type,
        'user_name': name,
    }

    return render(
        request,
        "role/main_menu.html",
        context,
    )


def upload(request):

    print request.GET
    if request.method == 'POST':
        if 'file' in request.FILES and request.FILES['file']:
            file = request.FILES['upfile']
        else:
            return HttpResponse('file null!')
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return HttpResponse('name null!')

        upload_file = Courseware(name=name,
                                 file=file)
        upload_file.save()

    else:
        return render(request, 'role/upload.html')

    return HttpResponse("successful")

# def download(request):
    # url = p.resource_file.path
    #     wrapper = FileWrapper(open(url, 'rb'))
    #     content_type = mimetypes.guess_type(url)
    #     response = HttpResponse(wrapper, content_type)
    #     response['Content-Disposition'] = "attachment; filename=%s" % 'test' + p.group.format
    #
    #     return response

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
    user.is_staff = 'True'
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


# 重命名文件名
def resource_file_path(instance, filename):
    file_time = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time()))
    filename = str(file_time) + instance.group.format
    return '/'.join([instance.group.name, 'resource', time.strftime('%m%d', time.localtime(time.time())), filename])

# Create your views here.
