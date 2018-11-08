import redis
import uuid
from io import BytesIO

from random import choice
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from course.models import Course, CourseOrg
from utils.captcha.hycaptcha import Captcha
from utils.dysms_python.demo_sms_send import send_sms
from .models import User, Banner
from .serializers import UserSerializer, UserRegistSerializer, SendSmsSerializer, UserInfoSerializer


class CustomBackend(ModelBackend):
    """
    重写验证方法
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class LoginView(APIView):

    def get(self, request):
        next_url = request.GET.get('next', '/')
        return render(request, 'login.html', {"next": next_url})

    def post(self, request):
        next_url = request.GET.get('next', '/')
        form_data = UserSerializer(data=request.data)
        if form_data.is_valid():
            username = form_data.validated_data['username']
            password = form_data.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                request.session.set_expiry(0)
                return redirect(next_url)

            else:
                return render(request, 'login.html', {'form_data': {'msg': '用户名或密码错误'}})

        else:
            return render(request, 'login.html', {'form_data': form_data.errors})


class SendSms(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    发送短信验证码
    """
    serializer_class = SendSmsSerializer

    @classmethod
    def createcode(cls):
        # 创建随机四位数验证码
        seeds = '0123456789'
        code = ''
        for i in range(4):
            code += choice(seeds)
        params = {"code": code}

        return params

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = SendSms.createcode()
        result = eval(send_sms(mobile, template_param=code))

        # 将验证码存在redis中
        if result['Code'] != 'OK':
            return Response(data=result['Message'], status=status.HTTP_400_BAD_REQUEST)
        else:
            connection_pool = redis.ConnectionPool(host='119.23.46.9', port='6379')
            _redis = redis.Redis(connection_pool=connection_pool)
            user_id = uuid.uuid4().hex
            _redis.hset(user_id, 'mobile_code', code['code'])
            _redis.expire(user_id, 600)
            result['uuid'] = user_id
            return Response(data=result, status=status.HTTP_200_OK)


# 生成图形验证码
def img_captcha(request):
    text, image = Captcha.gene_code()

    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    connection_pool = redis.ConnectionPool(host='119.23.46.9', port='6379')
    _redis = redis.Redis(connection_pool=connection_pool)
    _redis.set('img_captcha', text, 600)

    return response


class RegistView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    用户注册
    """
    serializer_class = UserRegistSerializer

    def get(self, request):
        return render(request, 'register.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return render(request, 'register.html', {"form_data": serializer.errors})

        user = self.perform_create(serializer)
        login(request, user)
        return render(request, 'index.html')

    def perform_create(self, serializer):
        return serializer.save()


class UserCenter(APIView):
    """
    用户个人中心
    """

    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login/?next="/user_center/"')
        return render(request, 'usercenter-info.html')

    def post(self, request):
        serializer_data = UserInfoSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'status':'success'})

        else:
            return Response({'status':'fail'})


class IndexView(APIView):
    """
    首页
    """
    def get(self, request):

        courses = Course.objects.all().order_by('-fav_nums')[:6]
        banner_courses = Course.objects.filter(is_banner=1)
        course_orgs = CourseOrg.objects.all().order_by('-fav_nums')
        banners = Banner.objects.all()

        return render(request, 'index.html', {'courses': courses,
                                              'course_orgs': course_orgs,
                                              'banner_courses':banner_courses,
                                              'banners':banners})



def page_not_found(request):

    return render(request, '404.html')







