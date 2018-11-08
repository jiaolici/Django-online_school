from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import UserFavorite

from .serializers import UserAskSerializer


class UserAskView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    用户咨询
    """
    serializer_class = UserAskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserFavView(APIView):

    def post(self, request):

        if request.user.is_anonymous:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        exist = UserFavorite.objects.filter(user_id=request.user.id, fav_id=fav_id, fav_type=fav_type)

        if exist:
            exist.delete()
            return HttpResponse('{"status":"success", "msg": "收藏"}', content_type='application/json')
        else:
            if fav_type > 0 and fav_id > 0:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user_id = request.user.id
                user_fav.save()
                return HttpResponse('{"status": "success", "msg":"已收藏"}',content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏"}', content_type='application/json')






