from rest_framework import status, views
from rest_framework.response import Response

from .usecases import PrefectureUsecase


class PrefectureView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = PrefectureUsecase().feed(user_id=request.user.id)
            return Response(data=data, status=status.HTTP_200_OK)
        except RuntimeError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
