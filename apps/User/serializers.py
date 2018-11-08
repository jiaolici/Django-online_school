__author__ = 'Miracle'
__date__ = '2018/11/3 10:41'

import redis
import re
from rest_framework import serializers
from.models import User


class UserSerializer(serializers.Serializer):
    """
    用户序列化
    """
    username = serializers.CharField(required=True, min_length=5)
    password = serializers.CharField(required=True, min_length=6)


class SendSmsSerializer(serializers.Serializer):
    """
    短信验证码
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        判断号码是否注册以及是否合法
        """
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError('该用户已经注册')

        mobile = re.findall('^1[2-9]\d{9}', mobile)[0]
        if not mobile:
            raise serializers.ValidationError('请输入合法的电话号码')

        return mobile


class UserRegistSerializer(serializers.ModelSerializer):
    """
    用户注册验证
    """
    mobile_code = serializers.CharField(max_length=4, error_messages={"max_length": '验证码只能为四位',
                                                                      "min_length": '验证码只能为四位',
                                                                      "required": '验证码不能为空'})
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    uuid = serializers.CharField(default='', max_length=32)

    img_captcha = serializers.CharField(min_length=4, error_messages={"max_length": '验证码只能为四位',
                                                                      "min_length": '验证码只能为四位',
                                                                      "required": '验证码不能为空'})

    def validate(self, attrs):
        connection_pool = redis.ConnectionPool(host='119.23.46.9', port='6379')
        _redis = redis.Redis(connection_pool=connection_pool)

        uuid = attrs['uuid']
        if int(_redis.hget(uuid, 'mobile_code')) == int(attrs['mobile_code']):
            if str(_redis.get('img_captcha').decode('utf8')).lower() == str(attrs['img_captcha']).lower():
                del attrs['uuid']
                del attrs['mobile_code']
                del attrs['img_captcha']
                attrs['mobile'] = attrs['username']
                return attrs
            else:
                raise serializers.ValidationError('图形验证码输入有误')
        else:
            raise serializers.ValidationError('短信验证码输入有误')

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'mobile_code', 'uuid', 'img_captcha')


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'birthday', 'gender', 'mobile', 'email')