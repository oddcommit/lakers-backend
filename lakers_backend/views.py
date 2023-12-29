from rest_framework import status, views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@permission_classes([AllowAny])
class HealthCheckView(views.APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            return Response(status=status.HTTP_200_OK)
        except RuntimeError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
