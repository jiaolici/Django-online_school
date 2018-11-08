"""online_school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve

import xadmin

from django.views.generic import TemplateView
from django.urls import path, include, re_path
from User.views import LoginView, RegistView, SendSms, img_captcha, UserCenter, IndexView, page_not_found
from organization.views import OrgListView, TeacherListView
from operation.views import UserAskView, UserFavView
from course.views import CourseListView, LessonView, course_token
from rest_framework.routers import DefaultRouter
from .settings import MEDIA_ROOT

router = DefaultRouter()
# 注册路由
router.register('regist', RegistView, basename='regist')

# 发送短信验证码
router.register('send_sms', SendSms, basename='send_sms')

# 机构列表
router.register('org_list', OrgListView, base_name='org')

# 用户咨询
router.register('user_ask', UserAskView, base_name='userask')

# 课程列表
router.register('course_list', CourseListView, base_name='course')

# 章节列表
router.register('lesson', LessonView, base_name='lesson')

# 讲师列表
router.register('teacher_list', TeacherListView, base_name='teacher')

urlpatterns = [
    # 后台管理
    path('admin/', xadmin.site.urls),

    # 主页
    path('', IndexView.as_view(), name='index'),

    # 登陆页
    path('login/', LoginView.as_view(), name='login'),

    # 用户收藏
    path('add_fav/', UserFavView.as_view(), name='user_fav'),

    # 图片验证码接口
    path('img_captcha/', img_captcha, name='img_captcha'),

    # 关联路由
    path('api-list/', include(router.urls)),

    # 视频接口

    path('video/', TemplateView.as_view(template_name='video.html')),
    path('course_token/', course_token, name='course_token'),

    # 个人中心
    path('user_center/', UserCenter.as_view(), name='user_center'),

    # 媒体文件路由
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})

]

handler404 = page_not_found
