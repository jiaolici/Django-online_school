__author__ = 'Miracle'
__date__ = '2018/11/4 18:06'
import re
from rest_framework import serializers
from .models import UserAsk, UserFavorite


class UserAskSerializer(serializers.ModelSerializer):
    """
    用户咨询
    """


    def validate_mobile(self, mobile):
        try:
            mobile = re.findall('^1[2-9]\d{9}', mobile)[0]
        except Exception:
            raise serializers.ValidationError('请输入合法的电话号码')
        if not mobile:
            raise serializers.ValidationError('请输入合法的电话号码')

        return mobile

    class Meta:
        model = UserAsk
        fields = '__all__'


