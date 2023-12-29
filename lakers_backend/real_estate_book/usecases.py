from rest_framework import viewsets

from lakers_backend.domains.city.application_services import CityService
from lakers_backend.domains.prefecture.application_services import PrefectureService
from lakers_backend.domains.real_estate_book.application_services import (
    RealEstateReceptionBookFeedService,
)
from lakers_backend.domains.reception_book_import.application_services import (
    ReceptionBookImportService,
)
from lakers_backend.domains.user.application_services import UserService
from lakers_backend.user.repositories import UserReader

from ..option.city.repositories import CityReader
from ..option.prefecture.repositories import PrefectureReader
from .repositories import RealEstateReceptionBookReader, ReceptionBookImportReader
from .serializers import (
    RealEstateReceptionBookFeedResponseSerializer,
    RealEstateReceptionBookImportStatusResponseSerializer,
)
from .types import ImportStatusListResponse, RequestType, ResponseType


class RealEstateReceptionBookFeedUsecase(viewsets.ModelViewSet):
    def feed(self, user_id: int, args: RequestType) -> ResponseType:
        # ここで有料プランと無料プランを分けて検索するロジックを加える
        # ここにフリープランを挿入
        is_superuser = self.is_super_user(user_id)
        args = self.convert_for_search_real_estate_books(
            user_id=user_id, is_superuser=is_superuser, args=args
        )
        domain_list, count = RealEstateReceptionBookFeedService(
            reader=RealEstateReceptionBookReader(), data=args
        ).execute(user_id, is_superuser)

        return {
            "count": count,
            "list": list(
                RealEstateReceptionBookFeedResponseSerializer(
                    domain_list, many=True
                ).data
            ),
        }

    @staticmethod
    def is_super_user(user_id: int) -> bool:
        is_super_user = UserService(UserReader(), user_id).is_superuser()
        return is_super_user

    @staticmethod
    def get_target_prefecture_ids(
        user_id: int, is_superuser: bool, prefectures_base: list[str]
    ):
        if len(prefectures_base) > 0:
            return prefectures_base
        prefectures = PrefectureService(
            reader=PrefectureReader(), user_id=user_id, is_superuser=is_superuser
        ).get_prefecture_ids()
        return prefectures

    @staticmethod
    def get_target_city_ids(
        user_id: int,
        is_superuser: bool,
        prefectures: list[str],
        base_city_ids: list[str],
    ):
        if len(base_city_ids) > 0:
            return base_city_ids
        cities = CityService(
            reader=CityReader(),
            user_id=user_id,
            is_superuser=is_superuser,
            data={"pref_codes": prefectures},
        ).get_normal_city_user_ids()
        return cities

    def convert_for_search_real_estate_books(
        self, user_id: int, is_superuser: bool, args: RequestType
    ) -> RequestType:
        if is_superuser:
            return args
        args["prefectures"] = self.get_target_prefecture_ids(
            user_id, is_superuser, args["prefectures"]
        )
        args["cities"] = self.get_target_city_ids(
            user_id, is_superuser, args["prefectures"], args["cities"]
        )
        return args


class RealEstateReceptionBookImportStatusUseCase(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs) -> ImportStatusListResponse:
        entity_list = ReceptionBookImportService(
            reader=ReceptionBookImportReader(), data=None
        ).execute()
        return {
            "list": list(
                RealEstateReceptionBookImportStatusResponseSerializer(
                    entity_list, many=True
                ).data
            )
        }
