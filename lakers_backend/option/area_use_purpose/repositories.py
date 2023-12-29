from data_models.models import (
    AreaUsePurpose,
    AreaUsePurposeConditions,
    AreaUsePurposeType,
)
from lakers_backend.domains.area_use_purpose.repositories import IAreaUsePurpose


class AreaUsePurposeReader(IAreaUsePurpose):
    @staticmethod
    def get_area_use_purpose_conditions(
        pref_name: str, city_code: str
    ) -> AreaUsePurposeConditions:
        return AreaUsePurposeConditions.objects.filter(
            prefecture_city__prefectures__name=pref_name,
            prefecture_city__city__city_code=city_code,
        ).get()

    @staticmethod
    def get_or_create_use_purpose_type(
        purpose_code: str, purpose_name: str
    ) -> AreaUsePurposeType:
        if not AreaUsePurposeType.objects.filter(
            area_use_purpose_type=purpose_code
        ).exists():
            return AreaUsePurposeType.objects.create(
                area_use_purpose_type=purpose_code, name=purpose_name
            )
        return AreaUsePurposeType.objects.filter(
            area_use_purpose_type=purpose_code
        ).get()

    @staticmethod
    def get_area_use_purpose(pref_name: str, city_code: str) -> list[AreaUsePurpose]:
        return AreaUsePurpose.objects.filter(
            prefecture_city__prefectures__name=pref_name,
            prefecture_city__city__city_code=city_code,
        ).all()

    @staticmethod
    def get_area_use_purpose_from_pref_name_and_city_name(
        pref_name: str, city_name: str
    ) -> list[AreaUsePurpose]:
        return AreaUsePurpose.objects.filter(
            prefecture_city__prefectures__name=pref_name,
            prefecture_city__city__name=city_name,
        ).all()
