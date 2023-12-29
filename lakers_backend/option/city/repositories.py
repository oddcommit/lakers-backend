from django.db.models import Q

from data_models.models import City, PrefecturesCity, UserPlan
from lakers_backend.domains.city.objects import DCity
from lakers_backend.domains.city.repositories import ICityReader

from .types import EncodedRequestType


class CityReader(ICityReader):
    """
    DBアクセスのreadの実体
    """

    def read(
        self, user_id: int, is_superuser: bool, data: EncodedRequestType
    ) -> list[DCity]:
        if is_superuser:
            return self.read_superuser(data)
        cities = self.build_normal_user_query_base(
            user_id=user_id, data=data
        ).values_list("city_id", "city__name", "city__city_code", "prefectures_id")

        result = [
            DCity(id=city[0], name=city[1], city_code=city[2], pref_code=city[3])
            for city in cities
        ]
        return result

    def get_normal_city_user_ids(
        self, user_id: int, data: EncodedRequestType
    ) -> list[str]:
        city_ids = self.build_normal_user_query_base(user_id, data).values_list(
            "city__id",
        )
        return [city_id[0] for city_id in city_ids]

    def build_normal_user_query_base(self, user_id: int, data: EncodedRequestType):
        return PrefecturesCity.objects.filter(
            self.build_filter(user_id, data["pref_codes"])
        ).exclude(city=City.objects.filter(name="不明").get())

    @staticmethod
    def build_filter_for_superuser(pref_codes: list[str]):
        city_filter = Q(prefectures__pref_code__in=pref_codes)
        return city_filter

    @staticmethod
    def build_filter(user_id: int, pref_codes: list[str]):
        pref_city_related_plans = UserPlan.objects.filter(user__id=user_id).all()

        prefectures_plan = set(
            [
                prefecture_related_plan.plan.plan_area.prefecture_code.pref_code
                for prefecture_related_plan in pref_city_related_plans
            ]
        )

        city_ids = set(
            [
                prefecture_related_plan.plan.plan_area.city_code.id
                for prefecture_related_plan in pref_city_related_plans
            ]
        )

        pref_code_for_search_target = set(pref_codes) & prefectures_plan

        city_filter = Q(
            prefectures__pref_code__in=pref_code_for_search_target,
            city__id__in=city_ids,
        )
        return city_filter

    def read_superuser(self, data: EncodedRequestType):
        city_and_pref_list = (
            PrefecturesCity.objects.filter(
                self.build_filter_for_superuser(data["pref_codes"])
            )
            .exclude(city=City.objects.filter(name="不明").get())
            .values_list("city_id", "city__name", "city__city_code", "prefectures_id")
            .order_by("city__city_code")
            .all()
        )

        result = [
            DCity(id=city[0], name=city[1], city_code=city[2], pref_code=city[3])
            for city in city_and_pref_list
        ]

        return result

    @staticmethod
    def get_prefecture_name_from_city_code(city_code: str) -> str | None:
        try:
            return (
                PrefecturesCity.objects.filter(city__city_code=str(city_code))
                .values_list("prefectures__name")
                .get()[0]
            )
        except PrefecturesCity.DoesNotExist:
            print(f"{city_code} has not found")
            return None

    @staticmethod
    def get_prefecture_city_from_names(
        pref_name: str, city_name: str
    ) -> list[PrefecturesCity]:
        return PrefecturesCity.objects.filter(
            prefectures__name=pref_name, city__name__startswith=city_name
        ).all()

    @staticmethod
    def get_prefecture_city_by_pref_name_and_city_code(
        pref_name: str, city_code: str
    ) -> PrefecturesCity:
        return PrefecturesCity.objects.filter(
            prefectures__name=pref_name,
            city__city_code=city_code,
        ).get()
