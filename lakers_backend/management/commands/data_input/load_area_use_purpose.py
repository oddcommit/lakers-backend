import geopandas as gpd
import pandas as pd
import swifter  # NOQA pylint: disable=W0611 並列化のためにインポートする必要あるため 仕様上構文解析に乗らず使われていない扱いになってしまう
from shapely.geometry import MultiPolygon, Point, Polygon, shape

from data_models.models import AreaUsePurpose

from .geojson import load_geojson
from .geometry import KokudoChiriinAPIAccessor
from .load_data_common import (
    load_all_properties_from_file_paths_common,
    load_file_paths,
)

PolygonBase = list[list[list[float]]]
MultiPolygonBase = list[list[list[list[float]]]]


def load_params(file_path: str) -> pd.DataFrame:
    df = load_geojson(file_path)
    return df.rename(  # pylint: disable=E1101
        columns={
            "A29_001": "行政区域コード",
            "A29_002": "都道府県名",
            "A29_003": "市区町村名",
            "A29_004": "用途地域コード",
            "A29_005": "用途地域名",
            "A29_006": "建蔽率",
            "A29_007": "容積率",
            "A29_008": "備考",
        }
    )


def load_area_use_purposes(dir_path: str) -> pd.DataFrame:
    paths = load_file_paths(dir_path, False)
    return load_all_properties_from_file_paths_common(paths, load_params)


def get_city_code(polygons: list[list[list[list[float]]]]) -> str:
    centroid = calc_centroid(polygons)
    return get_city_code_from_lat_lon(centroid)


def get_city_code_from_lat_lon(centroid: Point) -> str:
    api_accessor = KokudoChiriinAPIAccessor()
    results = api_accessor.fetch_address(str(centroid.x), str(centroid.y))
    return convert_kokudo_geo_api_result_to_city_code(results)


def convert_kokudo_geo_api_result_to_city_code(api_result: dict[str, str]) -> str:
    city_code = api_result["muniCd"]
    if len(city_code) == 0:
        return "99999"
    if city_code[0] == "0":
        return city_code[1:]
    return city_code


def calc_centroid(polygons: list[list[list[list[float]]]]) -> Point:
    target = Polygon(polygons[0])
    return target.centroid


def find_within_polygon(
    base_loc_x: float, base_loc_y: float, targets: list[AreaUsePurpose]
) -> AreaUsePurpose | None:
    if len(targets) < 1:
        return None
    base_pos = Point(base_loc_x, base_loc_y)
    master_df_base = {
        "location": [target for target in targets],
        "geometry": [build_polygon(target.geometry["geometry"]) for target in targets],
    }
    master_df = gpd.GeoDataFrame(master_df_base)
    result_df = master_df[base_pos.within(master_df["geometry"])]
    if len(result_df) < 1:
        return None
    return result_df.iloc[0]["location"]


def is_polygon_base(
    base_polygon: PolygonBase | MultiPolygonBase,
):
    return type(base_polygon[0][0][0]) is not list


def build_polygon(
    base_polygon: PolygonBase | MultiPolygonBase,
) -> Polygon | MultiPolygon:
    polygon_type = "Polygon" if is_polygon_base(base_polygon) else "MultiPolygon"
    polygon: MultiPolygon | Polygon = shape(
        {"type": polygon_type, "coordinates": base_polygon}
    )
    return polygon
