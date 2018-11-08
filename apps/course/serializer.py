from rest_framework import serializers
from .models import Course, Lesson
from organization.serializers import OrgSerializer


class CourseSerializer(serializers.ModelSerializer):

    course_org = OrgSerializer()

    class Meta:

        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:

        model = Lesson
        fields = '__all__'
