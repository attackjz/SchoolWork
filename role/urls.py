from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.Regist.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^regist/$', views.Regist.as_view(), name='regist'),
    url(r'^upload/$', views.upload, name='upload'),
]
