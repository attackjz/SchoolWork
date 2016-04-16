# coding=utf-8

from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
     url(r'^$', views.LoginView.as_view(), name='login'),
     url(r'^sign_in/$', views.sign_in, name='sign_in'),
     url(r'^sign_out/$', views.sign_out, name='sign_out'),
]
