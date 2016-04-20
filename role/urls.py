from django.conf.urls import url, include
from django.contrib import admin
from role import views


urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^regist/$', views.Regist.as_view(), name='regist'),
    url(r'^register/$', views.register, name='register'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/$', views.download, name='download'),
    url(r'^delete/$', views.Delete, name='delete'),
]
