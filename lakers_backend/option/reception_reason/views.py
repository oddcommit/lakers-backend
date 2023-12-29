from rest_framework import status, views
from rest_framework.response import Response

from .usecases import ReceptionReasonUsecase


class ReceptionReasonView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = ReceptionReasonUsecase().feed()
            return Response(data=data, status=status.HTTP_200_OK)
        except RuntimeError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
