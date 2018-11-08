__author__ = 'Miracle'
__date__ = '2018/11/4 11:42'

from rest_framework import serializers
from .models import CourseOrg, CityDict, Teacher


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CityDict
        fields = ('name',)


class OrgSerializer(serializers.ModelSerializer):
    """
    课程机构序列化
    """
    city = CitySerializer()

    class Meta:
        model = CourseOrg
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    """
    讲师序列化
    """
    class Meta:
        model = Teacher
        fields = '__all__'

