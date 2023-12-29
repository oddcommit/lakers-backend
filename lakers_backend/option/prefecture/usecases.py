from rest_framework import viewsets

from lakers_backend.domains.prefecture.application_services import PrefectureService
from lakers_backend.domains.user.application_services import UserService
from lakers_backend.user.repositories import UserReader

from .repositories import PrefectureReader
from .serializers import PrefectureResponseSerializer
from .types import ResponseType


class PrefectureUsecase(viewsets.ModelViewSet):
    def feed(self, user_id: int) -> ResponseType:
        is_super_user = self.is_super_user(user_id)
        domain_list = PrefectureService(
            reader=PrefectureReader(), user_id=user_id, is_superuser=is_super_user
        ).execute()
        return {"list": list(PrefectureResponseSerializer(domain_list, many=True).data)}

    @staticmethod
    def is_super_user(user_id: int) -> bool:
        is_super_user = UserService(UserReader(), user_id).is_superuser()
        return is_super_user
