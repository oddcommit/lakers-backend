"""
北海道は､全体として12系とした（北海道は、11系､12系、13系に属す）
東京都は､全体として9系とした（東京は、9系､14系､18系､19系に属す）
鹿児島県は､全体として2系とした（鹿児島県は、1系､2系に属す）
沖縄県は､全体として15系とした（沖縄県は、15系､16系､17系に属す）

参考）https://www.sinfonica.or.jp/faq/gis/minf_hzahyo.html
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

PREF_EPSG_CODE = {
    "北海道": 6680,
    "青森県": 6678,
    "岩手県": 6678,
    "宮城県": 6678,
    "秋田県": 6678,
    "山形県": 6678,
    "福島県": 6677,
    "茨城県": 6677,
    "栃木県": 6677,
    "群馬県": 6677,
    "埼玉県": 6677,
    "千葉県": 6677,
    "東京都": 6677,
    "神奈川県": 6677,
    "新潟県": 6676,
    "富山県": 6675,
    "石川県": 6675,
    "福井県": 6674,
    "山梨県": 6676,
    "長野県": 6676,
    "岐阜県": 6675,
    "静岡県": 6676,
    "愛知県": 6675,
    "三重県": 6674,
    "滋賀県": 6674,
    "京都府": 6674,
    "大阪府": 6674,
    "兵庫県": 6673,
    "奈良県": 6674,
    "和歌山県": 6674,
    "鳥取県": 6673,
    "島根県": 6671,
    "岡山県": 6673,
    "広島県": 6671,
    "山口県": 6671,
    "徳島県": 6672,
    "香川県": 6672,
    "愛媛県": 6672,
    "高知県": 6672,
    "福岡県": 6670,
    "佐賀県": 6670,
    "長崎県": 6669,
    "熊本県": 6670,
    "大分県": 6670,
    "宮崎県": 6670,
    "鹿児島県": 6670,
    "沖縄県": 6683,
}

PUBLIC_COORDINATE_SYSTEM_EPSG_CODE = {
    "公共座標1系": 6669,
    "公共座標2系": 6670,
    "公共座標3系": 6671,
    "公共座標4系": 6672,
    "公共座標5系": 6673,
    "公共座標6系": 6674,
    "公共座標7系": 6675,
    "公共座標8系": 6676,
    "公共座標9系": 6677,
    "公共座標10系": 6678,
    "公共座標11系": 6679,
    "公共座標12系": 6680,
    "公共座標13系": 6681,
    "公共座標14系": 6682,
    "公共座標15系": 6683,
    "公共座標16系": 6684,
    "公共座標17系": 6685,
    "公共座標18系": 6686,
    "公共座標19系": 6687,
}


def _calc_by_system(
    coord_system_df: pd.DataFrame, pref_name: str, org_coord_system: str
) -> gpd.GeoDataFrame:
    """
    座標系別の面積計算
    """
    gdf = gpd.GeoDataFrame(coord_system_df, crs=4326)
    if org_coord_system == "任意座標系":
        epsg_code = PREF_EPSG_CODE[pref_name]
        gdf.crs = f"epsg:{epsg_code}"
    elif "公共座標" in org_coord_system:
        epsg_code = PUBLIC_COORDINATE_SYSTEM_EPSG_CODE[org_coord_system]
        gdf = gdf.to_crs(epsg=epsg_code)
    else:
        raise ValueError
    gdf["地積"] = gdf["geometry"].area
    return gdf


def _convert_to_multi_polygon(coords):
    return shape({"type": "MultiPolygon", "coordinates": coords})


def apply_calc_area(input_df: pd.DataFrame, pref_name: str) -> pd.DataFrame:
    col_names = list(input_df.columns)
    col_names.append("地積")
    input_df["geometry"] = input_df["coordinates"].apply(_convert_to_multi_polygon)
    result_df_list = []
    for coord_system_name, group_df in input_df.groupby("座標系"):
        gdf = _calc_by_system(group_df, pref_name, str(coord_system_name))
        result_df_list.append(
            pd.DataFrame(gdf[col_names])
        )  # 異なる座標系もconcatしたいのでGeoDataFrame -> DataFrameに戻す
    df = pd.concat(result_df_list)
    return df
