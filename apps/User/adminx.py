__author__ = 'Miracle'
__date__ = '2018/11/2 19:34'
import xadmin
from xadmin import views
from .models import *


class GlobalSetting:
    site_title = '后台管理系统'
    site_footer = '后台管理系统'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin:
    list_fields = ['code', 'send_type', 'email', 'send_time']
    search_fields = ['code', 'send_type', 'email']  # 搜索字段不能加时间
    filter_fields = ['code', 'send_type', 'email', 'send_time']


class BannerAdmin:
    list_fields = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    filter_fields = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
