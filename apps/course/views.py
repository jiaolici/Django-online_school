from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
import os,hmac,hashlib,time
from online_school import settings
from organization.models import CourseOrg
from utils import restful
from .models import Course, Lesson
from .serializer import CourseSerializer, LessonSerializer
from django.shortcuts import render


class CoursePagination(PageNumberPagination):
    """
    分页
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 10000


class CourseListView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    课程列表
    """
    queryset = Course.objects.all().order_by('-fav_nums')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def list(self, request, *args, **kwargs):
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            queryset = Course.objects.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data).data

        # return Response(data)
        return render(request, 'course-list.html', {"courses": data,
                                                    'pages': range(int(data['count'])//int(CoursePagination.page_size)),
                                                    'hot_courses':serializer.data[:3]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.click_nums += 1
        instance.save()
        course_org = CourseOrg.objects.filter(id=instance.id)
        tag = instance.tag
        if tag:
            _course = Course.objects.filter(tag=tag)[0]
        else:
            _course = []
        return render(request, 'course-detail.html', {'data': serializer.data,
                                                      'course_org': course_org[0],
                                                      'related_course':_course})


class LessonView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    章节
    """

    serializer_class = LessonSerializer

    def get_queryset(self):
        global c_id
        c_id = self.request.GET.get('c_id')
        return Lesson.objects.filter(course_id=c_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        course = Course.objects.filter(id=c_id)[0]
        # return Response(serializer.data)
        return render(request, 'course-video.html', {'datas':serializer.data,
                                                     'course':course})



def course_token(request):
    file = request.GET.get('video_url')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})

