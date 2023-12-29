import math

import pandas as pd
from django.db import transaction

from data_models.models import (
    AreaUsePurpose,
    Land,
    LandAreaUsePurpose,
    PrefecturesCity,
    RegistrationMap,
)
from lakers_backend.option.area_use_purpose.repositories import AreaUsePurposeReader
from lakers_backend.option.city.repositories import CityReader

from ..data_input.load_area_use_purpose import find_within_polygon


def get_prefecture_city(
    area_use_purpose: AreaUsePurpose | None, pref_name: str, city_code: str
) -> PrefecturesCity:
    if area_use_purpose is None:
        return CityReader.get_prefecture_city_by_pref_name_and_city_code(
            pref_name, city_code
        )
    return area_use_purpose.prefecture_city


def create_registration_map(target_param: pd.Series) -> RegistrationMap:
    with transaction.atomic():
        return RegistrationMap.objects.create(
            coordinate_type=target_param["座標系"],
            geometry={"geometry": target_param["coordinates"]},
            area=target_param["地積"],
            latitude=target_param["代表点緯度"],
            longitude=target_param["代表点経度"],
        )


def create_land_area_use_purpose(
    land: Land, area_use_purpose: AreaUsePurpose | None
) -> LandAreaUsePurpose | None:
    if area_use_purpose is None:
        return None
    with transaction.atomic():
        return LandAreaUsePurpose.objects.create(
            land=land,
            area_use_purpose=area_use_purpose,
        )


def create_land(
    target_param: pd.Series,
    land_prefecture_city: PrefecturesCity,
    registration_map: RegistrationMap,
) -> Land:
    with transaction.atomic():
        return Land.objects.create(
            location=target_param["所在"].split(target_param["地番"])[0],
            chiban=target_param["地番"],
            prefecture_city=land_prefecture_city,
            registration_map=registration_map,
            latitude=target_param["代表点緯度変換後"],
            longitude=target_param["代表点経度変換後"],
        )


def add_registration_map_and_land(target_param: pd.Series):
    if math.isnan(target_param["代表点緯度変換後"]):
        return None
    area_use_purpose_targets = AreaUsePurposeReader.get_area_use_purpose(
        target_param["都道府県名"], target_param["市区町村コード"]
    )
    area_use_purpose = find_within_polygon(
        target_param["代表点経度変換後"],
        target_param["代表点緯度変換後"],
        area_use_purpose_targets,
    )
    try:
        land_prefecture_city = get_prefecture_city(
            area_use_purpose, target_param["都道府県名"], target_param["市区町村コード"]
        )
    except PrefecturesCity.DoesNotExist:
        print(
            f"pref_name:{target_param['都道府県名']} city_name:{target_param['市区町村コード']} does not found"
        )
        return None
    registration_map = create_registration_map(target_param)
    land = create_land(target_param, land_prefecture_city, registration_map)
    return land, create_land_area_use_purpose(land, area_use_purpose)
