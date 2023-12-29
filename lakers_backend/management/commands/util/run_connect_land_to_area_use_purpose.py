from typing import Callable

from django.db import transaction

from data_models.models import AreaUsePurpose, Land, LandAreaUsePurpose
from lakers_backend.option.area_use_purpose.repositories import AreaUsePurposeReader
from lakers_backend.option.lands.repositories import LandsReader

from ..data_input.load_area_use_purpose import find_within_polygon
from .add_land import create_land_area_use_purpose


def get_area_use_purpose(target: Land):
    area_use_purpose_targets = (
        AreaUsePurposeReader.get_area_use_purpose_from_pref_name_and_city_name(
            target.prefecture_city.prefectures.name, target.prefecture_city.city.name
        )
    )
    if len(area_use_purpose_targets) == 0:
        return None
    return find_within_polygon(
        target.longitude,
        target.latitude,
        area_use_purpose_targets,
    )


def create_or_update_connect(target: Land, area_use_purpose: AreaUsePurpose):
    land_connection_param = LandsReader.get_connection_of_land_to_area_use_purpose(
        target.pk, area_use_purpose.pk
    )
    if land_connection_param is None:
        return create_land_area_use_purpose(target, area_use_purpose)
    with transaction.atomic():
        land_connection_param.land = target
        land_connection_param.area_use_purpose = area_use_purpose
        land_connection_param.save()
    return land_connection_param


def run_connected_an_target(
    target: Land,
    connect_land_area_use_purpose: Callable[[Land, AreaUsePurpose], LandAreaUsePurpose],
):
    area_use_purpose = get_area_use_purpose(target)
    return connect_land_area_use_purpose(target, area_use_purpose)


def build_connect_land_area_use_purpose(
    will_ignore_connected: bool,
) -> Callable[[Land, AreaUsePurpose], LandAreaUsePurpose]:
    if will_ignore_connected:
        return create_land_area_use_purpose
    return create_or_update_connect


def run_connect(targets: list[Land], will_ignore_connected: bool):
    connect_land_area_use_purpose = build_connect_land_area_use_purpose(
        will_ignore_connected
    )

    for target in targets:
        run_connected_an_target(target, connect_land_area_use_purpose)
