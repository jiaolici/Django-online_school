__author__ = 'Miracle'
__date__ = '2018/11/3 9:19'

import xadmin

from .models import *

class LessonInline:
    model = Lesson
    extra = 0


class CourseAdmin:
    list_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    filter_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    inlines = [LessonInline]

class LessonAdmin:
    list_fields = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']
    filter_fields = ['name', 'course__name', 'add_time']


xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Course, CourseAdmin)