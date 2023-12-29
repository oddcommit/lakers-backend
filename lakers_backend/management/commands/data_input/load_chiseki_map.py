from typing import Callable

import pandas as pd
import swifter  # NOQA pylint: disable=W0611 並列化のためにインポートする必要あるため 仕様上構文解析に乗らず使われていない扱いになってしまう

from lakers_backend.option.city.repositories import CityReader

from ..util.calc_area import apply_calc_area
from ..util.nayose import convert_ascii
from .geojson import load_geojson
from .geometry import build_location_df
from .load_data_common import (
    load_all_properties_from_file_paths_common,
    load_file_paths,
)


def load_all_properties_from_file_paths(
    file_paths: list[str], is_jsonl: bool = False
) -> pd.DataFrame:
    load_data = load_dataloader(is_jsonl)
    return load_all_properties_from_file_paths_common(file_paths, load_data)


def calc_chiseki(df: pd.DataFrame):
    """
    地積を算出
    :param df:
    :return:
    """
    prefectures = df["都道府県名"].unique()
    if len(prefectures) == 1:
        return apply_calc_area(df, prefectures[0])

    first_prefecture = prefectures[0]
    base_df = apply_calc_area(
        df.query(f"都道府県名.str=={first_prefecture}"), first_prefecture
    )
    for prefecture in prefectures[1:]:
        other_df = apply_calc_area(
            df.query(f"都道府県名.str=={prefecture}"), first_prefecture
        )
        base_df = pd.concat([base_df, other_df])

    return base_df


def load_jsonl(file_path: str):
    base_df = pd.read_json(file_path, orient="records", lines=True)
    print(f"file {file_path} has loaded")
    return base_df.rename(  # pylint: disable=E1101
        columns={
            "coordinate_system": "座標系",
            "map_name": "地図名",
            "district_name": "大字名",
            "sub_block_name": "小字名",
            "parcel_number": "地番",
            "municipality_name": "市区町村名",
            "block_name": "丁目名",
            "municipality_code": "市区町村コード",
            "reserved_name": "予備名",
            "matching_column": "所在",
            "representative_latitude": "代表点緯度",
            "representative_longitude": "代表点経度",
        }
    )


def load_all_properties(dir_path: str, is_jsonl: bool = False):
    df = load_raw_dataset_with_prefectures_info(dir_path, is_jsonl)
    return calc_chiseki(df)


def build_df_with_prefecture_name(df: pd.DataFrame) -> pd.DataFrame:
    df["都道府県名"] = build_prefecture_info_to_df(df)
    return df.dropna(subset=["都道府県名"])


def load_raw_dataset_with_prefectures_info(dir_path: str, is_jsonl: bool = False):
    df = load_raw_dataset(dir_path, is_jsonl)
    return build_df_with_prefecture_name(df)


def load_raw_dataset(dir_path: str, is_jsonl: bool = False):
    file_paths = load_file_paths(dir_path, is_jsonl)
    df = load_all_properties_from_file_paths(file_paths, is_jsonl)
    if is_jsonl:
        df.coordinates = df.coordinates.swifter.apply(eval)
        return df
    df.coordinates = df.coordinates.swifter.apply(eval)
    df["大字名"] = df["大字名"].apply(convert_ascii)
    df["小字名"] = df["小字名"].apply(convert_ascii)
    df["丁目名"] = df["丁目名"].apply(convert_ascii)
    df["予備名"] = df["予備名"].apply(convert_ascii)
    return df


def load_dataloader(is_jsonl: bool) -> Callable[[str], pd.DataFrame]:
    if is_jsonl:
        return load_jsonl
    return load_geojson


def build_prefecture_info_to_df(df: pd.DataFrame) -> pd.Series:
    return df.市区町村コード.apply(CityReader.get_prefecture_name_from_city_code)


def pickup_public_location_dataset(df: pd.DataFrame) -> pd.DataFrame:
    public_location_dataset = df.query('座標系.str.startswith("公共座標")')
    public_location_dataset["代表点緯度変換後"] = public_location_dataset["代表点緯度"]
    public_location_dataset["代表点経度変換後"] = public_location_dataset["代表点経度"]
    return public_location_dataset


def pickup_any_location_dataset(df: pd.DataFrame) -> pd.DataFrame:
    any_location_dataset = df.query('座標系.str.startswith("任意")')
    loc_df = build_location_df(any_location_dataset)
    any_location_dataset["代表点緯度変換後"] = loc_df["代表点緯度"]
    any_location_dataset["代表点経度変換後"] = loc_df["代表点経度"]
    return any_location_dataset


def build_location_dataset(df: pd.DataFrame) -> pd.DataFrame:
    public_df = pickup_public_location_dataset(df)
    any_df = pickup_any_location_dataset(df)
    return pd.concat([public_df, any_df])
