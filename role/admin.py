# coding=utf-8

from django.contrib import admin
from models import *
import models
# Register your models here.


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_staff',
                'groups',
            )
        }),
    )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'number',
        'user',
    )

admin.site.register(models.Teacher, TeacherAdmin)


class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'number',
        'user',
    )

admin.site.register(models.Student, StudentAdmin)


class TeamAdmin(admin.ModelAdmin):

    list_display = (
        'number',
        'grade',
    )

    filter_horizontal = (

        'teacher',
        'student',
    )


admin.site.register(models.Team, TeamAdmin)


class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'number',
        'name',
    )

    filter_horizontal = (
        'teacher',
        'team',
    )

admin.site.register(models.Subject, SubjectAdmin)


class CoursewareAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'pub_datetime',
    )

    def get_queryset(self, request):
        qs = super(CoursewareAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        t = Teacher.objects.get(user=request.user)
        s_list = Subject.objects.filter(teacher=t)
        return qs.filter(subject=s_list)

    # def queryset(self):
    #     qs = super(CoursewareAdmin, self).queryset()
    #     t = Teacher.objects.get(user=self.requst.user)
    #     s_list = Subject.objects.filter(teacher=t)
    #     return qs.filter(teacher=s_list)

admin.site.register(models.Courseware, CoursewareAdmin)
