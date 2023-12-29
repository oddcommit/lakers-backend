from rest_framework import status, views
from rest_framework.response import Response

from .usecases import (
    RealEstateReceptionBookFeedUsecase,
    RealEstateReceptionBookImportStatusUseCase,
)


class RealEstateReceptionBookFeedView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            params_base = request.query_params.dict()
            params_base["cities"] = request.query_params.getlist("cities[]")
            params_base["prefectures"] = request.query_params.getlist("prefectures[]")
            params_base["reception_reasons"] = request.query_params.getlist(
                "reception_reasons[]"
            )
            data = RealEstateReceptionBookFeedUsecase().feed(
                user_id=request.user.id, args=params_base
            )
            return Response(data=data, status=status.HTTP_200_OK)
        except RuntimeError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RealEstateReceptionBookImportStatusView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = RealEstateReceptionBookImportStatusUseCase().list(
                request, *args, **kwargs
            )
            return Response(data=data, status=status.HTTP_200_OK)
        except RuntimeError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
