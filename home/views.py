# coding=utf-8

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views import generic
import datetime
from django.contrib.auth import models, authenticate, login, logout
# Create your views here.


class LoginView(generic.View):

    templates_file = 'home/index.html'

    def get(self, request):

        if request.user.is_authenticated():
            return HttpResponseRedirect('/role/home')

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
            if error_code == '1':
                error_txt = "用户名或密码不能为空"
            elif error_code == '2':
                error_txt = "用户名与密码不匹配或该用户不存在"
            else:
                error_txt = "未知错误,请与管理员联系!"
        else:
            error_txt = ""

        context = {
            "error_txt": error_txt,
            "e": "waaaaa",
        }

        return render(request,
                      self.templates_file,
                      context)


def sign_in(request):

    if request.method == "POST":

        postdata = request.POST

        if 'username' in postdata and postdata['username'] and 'password' in postdata and postdata['password']:
            username = postdata['username']
            password = postdata['password']
        else:
            return HttpResponseRedirect("/?error=1")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/?error=2')

        # return render(request,
        #               'role/upload.html',
        #               )

    else:
        return render(
            request,
            '/role/home',
        )


def sign_out(request):

    logout(request)

    return HttpResponseRedirect('/')


def index(request):
    templates = 'home/index.html'
    # templates = 'role/regist.html'

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

    template = 'role/regist.html'
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

    template = 'role/regist.html'

    return render(
        request,
        template,
    )
