from datetime import datetime

import pandas as pd

from data_models.models import (
    AreaUsePurpose,
    AreaUsePurposeConditions,
    AreaUsePurposeType,
    PrefecturesCity,
)


class AreaUsePurposeFactory(object):
    @staticmethod
    def build_area_use_purpose_conditions() -> list[AreaUsePurposeConditions]:
        raw_csv_path = "tests/application/option/area_use_purpose/data/data_models_areausepurposeconditions.csv"
        df = pd.read_csv(raw_csv_path)
        return [
            AreaUsePurposeConditions.objects.create(
                id=params.id,
                miniature=params.miniature,
                conditions=params.conditions,
                prefecture_city=PrefecturesCity.objects.filter(
                    pk=params.prefecture_city_id
                ).get(),
                publish_flag=params.publish_flag,
                published_at=datetime.now(),
            )
            for _, params in df.iterrows()
        ]

    @staticmethod
    def build_area_use_purpose_type() -> list[AreaUsePurposeType]:
        raw_csv_path = "tests/application/option/area_use_purpose/data/data_models_areausepurposetype.csv"
        df = pd.read_csv(raw_csv_path)
        return [
            AreaUsePurposeType.objects.create(
                area_use_purpose_type=params.area_use_purpose_type,
                name=params.name,
            )
            for _, params in df.iterrows()
        ]

    @staticmethod
    def build_area_use_purpose(
        area_use_purpose_type: AreaUsePurposeType,
        area_use_purpose_conditions: AreaUsePurposeConditions,
        geometry: list[list[list[float]]] | list[list[list[list[float]]]],
        building_late: float = 0.5,
        volume_late: float = 0.5,
    ):
        return AreaUsePurpose.objects.create(
            prefecture_city=area_use_purpose_conditions.prefecture_city,
            area_use_purpose_type=area_use_purpose_type,
            area_use_purpose_condition=area_use_purpose_conditions,
            building_late=building_late,
            geometry={"geometry": geometry},
            volume_late=volume_late,
        )

    def init_area_use_purpose(
        self,
        has_initialized_purpose_conditions: bool = False,
        has_initialized_use_purpose_type: bool = False,
    ) -> list[AreaUsePurpose]:
        if not has_initialized_purpose_conditions:
            self.build_area_use_purpose_conditions()
        if not has_initialized_use_purpose_type:
            self.build_area_use_purpose_type()
        raw_csv_path = "tests/application/option/area_use_purpose/data/data_models_areausepurpose.csv"
        df = pd.read_csv(raw_csv_path)

        return [
            AreaUsePurpose.objects.create(
                prefecture_city=PrefecturesCity.objects.filter(
                    id=params.prefecture_city_id
                ).get(),
                area_use_purpose_type=AreaUsePurposeType.objects.filter(
                    id=params.area_use_purpose_id
                ).get(),
                area_use_purpose_condition=AreaUsePurposeConditions.objects.filter(
                    id=params.area_use_purpose_condition_id
                ).get(),
                building_late=params.building_late,
                geometry={"geometry": params.geometry},
                volume_late=params.volume_late,
            )
            for _, params in df.iterrows()
        ]
