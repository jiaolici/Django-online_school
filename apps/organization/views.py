from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from .models import CourseOrg, Teacher, CityDict
from course.models import Course
from .serializers import OrgSerializer, TeacherSerializer
from operation.models import UserFavorite
# Create your views here.


class OrgListPagination(PageNumberPagination):
    """
    分页
    """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 10000


class OrgListView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    课程机构列表
    """
    queryset = CourseOrg.objects.all().order_by('fav_nums')
    serializer_class = OrgSerializer
    pagination_class = OrgListPagination

    def list(self, request, *args, **kwargs):
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            queryset = CourseOrg.objects.filter(Q(name__icontains=search_keyword)|Q(desc__icontains=search_keyword))
        else:
            city_id = self.request.GET.get('city', '')
            ct = self.request.GET.get('ct', '')
            if city_id:
                if ct:
                    queryset = CourseOrg.objects.filter(city_id=city_id, category=ct).order_by('fav_nums')
                else:
                    queryset = CourseOrg.objects.filter(city_id=city_id).order_by('fav_nums')
            else:
                if ct:
                    queryset = CourseOrg.objects.filter(category=ct).order_by('fav_nums')
                else:
                    queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        page_data = self.get_paginated_response(serializer.data).data
        all_city = CityDict.objects.all()
        return render(request, 'org-list.html', {'data': page_data,
                                                 "pages": range(int(page_data['count'])//int(OrgListPagination.page_size)),
                                                 'citys':all_city})

    def retrieve(self, request, *args, **kwargs):
        # 机构详情接口
        instance = self.get_object()
        instance.click_nums += 1
        instance.save()
        serializer = self.get_serializer(instance)
        course = Course.objects.filter(course_org_id=instance.id)
        teacher = Teacher.objects.filter(org_id=instance.id)
        if request.user.is_anonymous:
            is_fav = False
        else:
            if UserFavorite.objects.filter(user_id=request.user.id, fav_id=int(instance.id), fav_type=2):
                is_fav = True
            else:
                is_fav = False
        return render(request, 'org-detail-homepage.html', {'data': serializer.data,
                                                            "courses": course,
                                                            "teachers": teacher,
                                                            "is_fav": is_fav})


class TeacherListView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = Teacher.objects.all().order_by('-fav_nums')
    serializer_class = TeacherSerializer
    pagination_class = OrgListPagination

    def list(self, request, *args, **kwargs):
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            queryset = Teacher.objects.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data).data
        hot_teachers = data['results'][:3]

        return render(request, 'teachers-list.html', {'data': data,
                                                      "pages": range(int(data['count']) // int(OrgListPagination.page_size)),
                                                      'hot_teachers':hot_teachers})
        # return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        courses = Course.objects.filter(id=instance.id)
        hot_teachers = self.queryset[:3]
        return render(request, 'teacher-detail.html', {'teacher': serializer.data,
                                                       'courses': courses,
                                                       'hot_teachers':hot_teachers})




