import logging
import os
from collections import namedtuple

import numpy as np

from data_models.models import (
    AreaUsePurpose,
    Building,
    BuildingAreaUsePurpose,
    Land,
    LandAreaUsePurpose,
    Prefectures,
    PrefecturesCity,
    RealEstateReceptionBook,
)
from lakers_backend.management.commands.data_input.geometry import (
    KokudoChiriinAPIAccessor,
)
from lakers_backend.management.commands.data_input.load_area_use_purpose import (
    find_within_polygon,
)

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

BUILDING_TYPES = [
    1,  # 建物
    3,  # 区分建物
    6,  # 一棟
]


LAND_TYPES = [
    2,  # 土地
]

Point = namedtuple("Point", ["x", "y"])

POINT_CACHE: dict[str, Point] = {}


def find_area_use_purpose(
    longitude: float, latitude: float, target_prefectures_city: PrefecturesCity
) -> AreaUsePurpose | None:
    area_use_purpose_targets = AreaUsePurpose.objects.filter(
        prefecture_city=target_prefectures_city
    ).all()
    if len(area_use_purpose_targets) == 0:
        return None
    return find_within_polygon(
        longitude,
        latitude,
        area_use_purpose_targets,
    )


def geocoding(location) -> Point:
    if point := POINT_CACHE.get(location):
        return point
    api_accessor = KokudoChiriinAPIAccessor()
    lat_lon = api_accessor.fetch_lat_lon(location)
    latitude = lat_lon.get("代表点緯度", 0)
    longitude = lat_lon.get("代表点経度", 0)
    point = Point(longitude, latitude)
    if latitude != 0 and longitude != 0:
        POINT_CACHE[location] = point
    return point


def save_building(book: RealEstateReceptionBook):
    building = Building.objects.filter(
        prefecture_city=book.prefectures_city, kaoku_number=book.kaoku_number
    ).first()
    if not building:
        location = book.address
        point = geocoding(location)
        latitude, longitude = point.y, point.x
        if latitude == 0 and longitude == 0:
            return
        building = Building.objects.create(
            prefecture_city=book.prefectures_city,
            kaoku_number=book.kaoku_number,
            real_estate_type=book.real_estate_type,
            latitude=latitude,
            longitude=longitude,
        )
        book.building = building
        book.save()
        area_use_purpose = find_area_use_purpose(
            longitude=longitude,
            latitude=latitude,
            target_prefectures_city=book.prefectures_city,
        )
        if area_use_purpose is None:
            return
        BuildingAreaUsePurpose.objects.create(
            building=building, area_use_purpose=area_use_purpose
        )
    else:
        book.building = building
        book.save()


def save_land(book: RealEstateReceptionBook):
    chiban = book.chiban  # 正規化は不要そう
    land = Land.objects.filter(
        prefecture_city=book.prefectures_city, chiban=chiban
    ).first()
    if not land:
        location = book.address
        point = geocoding(location)
        latitude, longitude = point.y, point.x
        if latitude == 0 and longitude == 0:
            return None
        land = Land.objects.create(
            location=book.address,
            chiban=chiban,
            latitude=latitude,
            longitude=longitude,
            prefecture_city=book.prefectures_city,
        )
        book.land = land
        book.save()
        area_use_purpose = find_area_use_purpose(
            longitude=longitude,
            latitude=latitude,
            target_prefectures_city=book.prefectures_city,
        )
        if area_use_purpose is None:
            return
        LandAreaUsePurpose.objects.create(land=land, area_use_purpose=area_use_purpose)
    else:
        book.land = land
        book.save()


def load_land_and_building(pref_city: PrefecturesCity):
    POINT_CACHE.clear()
    for book in RealEstateReceptionBook.objects.filter(
        prefectures_city=pref_city
    ).order_by("real_estate_type"):
        if book.real_estate_type and book.real_estate_type.id in BUILDING_TYPES:
            save_building(book)
        elif book.real_estate_type and book.real_estate_type.id in LAND_TYPES:
            save_land(book)


def main():
    pref_objects = Prefectures.objects
    if target_prefectures := os.getenv("LAKERS_TARGET_PREFECTURES"):
        pref_objects = pref_objects.filter(pref_code__in=target_prefectures.split(","))
    for pref in pref_objects.order_by("pref_code").all():
        logger.info(f"{pref.name}の処理を開始します")
        pref_cities = (
            PrefecturesCity.objects.filter(prefectures__pref_code=pref.pref_code)
            .order_by("city_id")
            .all()
        )
        if target_cities_chunk := os.getenv("LAKERS_TARGET_CITIES_CHUNK"):
            # e.g. 1/5, 3/10(10分割したうちの3番目)
            chunk_idx, split_num = target_cities_chunk.split("/")
            pref_cities = np.array_split(pref_cities, int(split_num))[
                int(chunk_idx) - 1
            ]
            logger.info(f"{pref.name} 分割:{target_cities_chunk}")
        for pref_city in pref_cities:
            logger.info(f"{pref.name}{pref_city.city.name}の処理を開始します")
            if not os.getenv("LAKERS_BATCH_DRY_RUN"):
                load_land_and_building(pref_city)
            logger.info(f"{pref.name}{pref_city.city.name}の処理が終了しました")
        logger.info(f"{pref.name}の処理が終了しました")
