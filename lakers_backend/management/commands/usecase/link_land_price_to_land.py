import logging

import geopandas as gpd
import pandas as pd
from django.db.models import Exists, OuterRef
from django_pandas.io import read_frame
from shapely import Point

from data_models.models import Land, LinkLandPriceToLand, PublicLandPrice

logger = logging.getLogger(__name__)

LANDID = "land_id"
PUBLICLANDPRICEID = "public_land_price_id"
LATITUDE = "latitude"
LONGITUDE = "longitude"
COLUMNS = ("id", LATITUDE, LONGITUDE)


def main(add_data_type: str):
    # pylint: disable=W0719
    """メイン処理

    Args:
        add_data_type (str): landまたはland_priceしか受け付けない
    """

    # 公示価格データの年度リスト
    unique_years_list = PublicLandPrice.objects.distinct().values_list("year")

    for year in unique_years_list:
        # 対象年度の公示価格データを読み込み
        df_public_land_price = read_frame(
            PublicLandPrice.objects.filter(year=year[0]).values(*COLUMNS)
        )

        if add_data_type == "land":
            # 登録済みの土地データ以外
            df_land = read_frame(
                Land.objects.filter(
                    ~Exists(LinkLandPriceToLand.objects.filter(land_id=OuterRef("pk")))
                ).values(*COLUMNS)
            )

            intermediate_df = get_nearest_location(df_land, df_public_land_price)
            # DBへ登録
            if len(intermediate_df) != 0:
                bulk_create_intermediate_land_price(intermediate_df)

        elif add_data_type == "land_price":
            # 中間テーブルに存在しない土地IDのみのデータに絞る
            public_land_price_id_list = df_public_land_price["id"].to_list()
            intermediate_land_id_list = LinkLandPriceToLand.objects.values_list(
                PUBLICLANDPRICEID, flat=True
            )
            not_duplicate_list = list(
                set(public_land_price_id_list) & set(intermediate_land_id_list)
            )
            # 過去に登録したことのある年度はスキップ
            if len(not_duplicate_list) != 0:
                print(f"{year[0]}年度のデータ登録をスキップしました")
                continue

            chunk_size = 1000000
            total = Land.objects.all().count()
            loops = (total + 999999) // chunk_size

            # 土地データを分割しながらデータベースへ登録
            for i in range(loops):
                start = i * chunk_size
                if total > chunk_size:
                    total = total - chunk_size
                    end = (i + 1) * chunk_size
                else:
                    end = start + total

                print(f"{start}件目〜{end}件目を処理中です...")
                df_land = read_frame(Land.objects.all()[start:end])
                first_row_id = df_land["id"].iloc[0]
                last_row_id = df_land["id"].iloc[-1]

                # 土地IDとその土地に最も近い距離の公示価格IDを取得
                intermediate_df = get_nearest_location(df_land, df_public_land_price)

                print(f"土地ID: {first_row_id} ~ {last_row_id} の登録を開始します")
                # DBへ登録
                if len(intermediate_df) != 0:
                    bulk_create_intermediate_land_price(intermediate_df)
                    print(f"土地ID: {first_row_id} ~ {last_row_id} の登録が完了しました")


def get_nearest_location(
    df_land_mst: pd.DataFrame, df_land_price: pd.DataFrame
) -> pd.DataFrame:
    # pylint: disable=W0719

    # 緯度経度からPointオブジェクトを作る
    df_land_mst["geometry"] = [
        Point(x, y) for x, y in zip(df_land_mst[LONGITUDE], df_land_mst[LATITUDE])
    ]
    df_land_price["geometry"] = [
        Point(x, y) for x, y in zip(df_land_price[LONGITUDE], df_land_price[LATITUDE])
    ]

    # GeoDataFrameに変換
    gdf_df_land_mst = gpd.GeoDataFrame(df_land_mst)
    gdf_land_price = gpd.GeoDataFrame(df_land_price)

    # 最近傍地点を取得
    nearest_df = gpd.sjoin_nearest(
        gdf_df_land_mst, gdf_land_price, distance_col="distances", how="left"
    )

    nearest_df = nearest_df[["id_left", "id_right"]].rename(
        columns={"id_left": LANDID, "id_right": PUBLICLANDPRICEID}
    )

    return nearest_df


def bulk_create_intermediate_land_price(in_df: pd.DataFrame):
    # pylint: disable=W0719
    """DBへ登録"""
    intermediate_land_price_for_insert = [
        LinkLandPriceToLand(**row) for row in in_df.to_dict(orient="records")
    ]

    LinkLandPriceToLand.objects.bulk_create(intermediate_land_price_for_insert)
