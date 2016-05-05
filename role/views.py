# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.contrib.auth import models
from django.views import generic
from django import forms
from wsgiref.util import FileWrapper  # 引用下载


from role.models import *

import os
import models
import re
import time
import mimetypes # 下载

def index(request):
    # templates = 'role/regist.html'
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

    clicked = -1
    click_name = ''
    courseware_list = {}
    if 'clicked' in request.GET and request.GET['clicked']:
        click_id = request.GET['clicked']
        subject = Subject.objects.get(id=click_id)
        click_name = subject.name
        courseware = Courseware.objects.filter(subject=click_id)
        for i in courseware:
            print i
            courseware_list[str(i.id)] = i.name
        clicked = click_id
        print courseware_list

    return_info = ''
    if 'returninfo' in request.GET and request.GET['returninfo']:
        return_info = request.GET['returninfo']

    context = {
        'page_type': 'home',
        'msg ': 'sdawdaw',
        'subject_list': sub_list,
        'courseware_list': courseware_list,
        'user_type': user_type,
        'user_name': name,
        'click_id': clicked,
        'click_name': click_name,
        'returninfo': return_info,
    }

    return render(
        request,
        "role/main_menu.html",
        context,
    )


# 上传
def upload(request):

    print request.GET
    if request.method == 'POST':

        if 'subject' in request.POST and request.POST['subject']:
            click_id = request.POST['subject']
            subject = Subject.objects.get(id=click_id)

        if 'upfile' in request.FILES and request.FILES['upfile']:
            file = request.FILES['upfile']
        else:
            return HttpResponseRedirect('/role/home?returninfo=file&clicked=' + str(click_id))
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return HttpResponseRedirect('/role/home?returninfo=name&clicked=' + str(click_id))

        user = request.user
        teacher = Teacher.objects.get(user=user.id)

        upload_file = Courseware(name=name,
                                 file=file,
                                 teacher=teacher,
                                 )
        upload_file.save()
        upload_file.subject.add(subject)


    else:
        # return render(request, 'role:home')
        return HttpResponseRedirect('/role/home?returninfo=error')

    return HttpResponseRedirect('/role/home?returninfo=success&clicked=' + str(click_id))


def download(request):

    if 'download' in request.GET and request.GET['download']:
        d = request.GET['download']
    else:
        return HttpResponseRedirect('/')

    if 'clicked' in request.GET and request.GET['clicked']:
        c = request.GET['clicked']
    else:
        return HttpResponseRedirect('/')

    courseware = Courseware.objects.get(id=d)
    url = courseware.file.path
    if os.path.exists(url):
        format = re.findall('\.\w+$', url)

        wrapper = FileWrapper(open(url, 'rb'))
        content_type = mimetypes.guess_type(url)
        response = HttpResponse(wrapper, content_type)
        filename = courseware.name + format[0]
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response
    else:
        return_url = '/role/home?clicked=' + str(c) + '&returninfo=download_error'
        return HttpResponseRedirect(return_url)


def Delete(request):

    if 'delete' in request.GET and request.GET['delete']:
        d = request.GET['delete']
    else:
        return HttpResponseRedirect('/')

    if 'clicked' in request.GET and request.GET['clicked']:
        c = request.GET['clicked']
    else:
        return HttpResponseRedirect('/')

    courseware = Courseware.objects.get(id=d)

    url = courseware.file.path
    if os.path.exists(url):
        os.remove(url)

    courseware.delete()

    return_url = '/role/home?clicked=' + str(c) + '&returninfo=delete'
    return HttpResponseRedirect(return_url)


class Regist(generic.View):

    template_name = 'role/regist.html'

    def get(self, request):

        if not request.user.is_superuser:
            return HttpResponseRedirect("/")

        info = ''

        if 'info' in request.GET and request.GET['info']:
            info = request.GET['info']

        context = {
            'info': info
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
    first = post_data['first']
    last = post_data['last']

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

    if first:
        user.first_name = first
        user.save()

    if last:
        user.last_name = last
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

    return HttpResponseRedirect('/role/regist?info=success')

# Create your views here.
