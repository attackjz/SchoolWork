# coding=utf-8
from django.contrib import admin
import models
from models import Choice, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollsAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'pub_date',
        'back2',
    )
    inlines = [ChoiceInline]
    list_filter = ['question_text']

    def back2(self, wqe):
        return '2333'
    back2.allow_tags = True

# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = (
#         'choice_text',
#         'votes',
#     )



admin.site.register(models.Poll, PollsAdmin)
# admin.site.register(models.Choice, ChoiceAdmin)
# Register your models here.
