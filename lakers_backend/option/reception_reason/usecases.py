from rest_framework import viewsets

from lakers_backend.domains.real_estate_book.application_services import (
    ReceptionReasonFeedService,
)

from .repositories import ReceptionReasonReader
from .serializers import ReceptionReasonResponseSerializer
from .types import ResponseType


class ReceptionReasonUsecase(viewsets.ModelViewSet):
    def feed(self) -> ResponseType:
        domain_list = ReceptionReasonFeedService(
            reader=ReceptionReasonReader(),
        ).execute()

        return {
            "list": list(ReceptionReasonResponseSerializer(domain_list, many=True).data)
        }
