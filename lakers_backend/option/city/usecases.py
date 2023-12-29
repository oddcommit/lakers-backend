from rest_framework import viewsets

from lakers_backend.domains.city.application_services import CityService
from lakers_backend.domains.prefecture.application_services import PrefectureService
from lakers_backend.domains.user.application_services import UserService
from lakers_backend.user.repositories import UserReader

from ..prefecture.repositories import PrefectureReader
from .repositories import CityReader
from .serializers import CityResponseSerializer
from .types import EncodedRequestType, ResponseType


class CityUsecase(viewsets.ModelViewSet):
    def feed(self, user_id: int) -> ResponseType:
        is_superuser = self.is_super_user(user_id)
        domain_list = CityService(
            reader=CityReader(),
            user_id=user_id,
            is_superuser=is_superuser,
            data=self.build_args(user_id, is_superuser),
        ).execute()

        return {"list": list(CityResponseSerializer(domain_list, many=True).data)}

    @staticmethod
    def build_args(user_id: int, is_superuser: bool) -> EncodedRequestType:
        if is_superuser:
            return {"pref_codes": ["11", "12", "13", "14"]}
        prefs = PrefectureService(
            reader=PrefectureReader(), user_id=user_id, is_superuser=is_superuser
        ).get_prefecture_ids()
        return {"pref_codes": prefs}

    @staticmethod
    def is_super_user(user_id: int) -> bool:
        is_super_user = UserService(UserReader(), user_id).is_superuser()
        return is_super_user
