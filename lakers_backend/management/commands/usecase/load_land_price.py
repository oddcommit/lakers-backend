import json
import logging
import re
import unicodedata

import numpy as np
import pandas as pd
from django.db.models import Q
from django_pandas.io import read_frame
from pandas import json_normalize

from data_models.models import Prefectures, PublicLandPrice

logger = logging.getLogger(__name__)

NENDO_RAW = "L01_005"
LAND_PRICE_RAW = "L01_006"
SYOZAI_CHIBAN_RAW = "L01_024"
JUKYO_HYOJI_RAW = "L01_025"
NENDO = "year"
LAND_PRICE = "land_price"
JUKYO_HYOJI = "jukyo_hyoji"
TODOFUKEN = "todofuken"
SYOZAI_CHIBAN = "syozai_chiban"
SYOZAI = "location"
CHIBAN = "chiban"
PREF_CODE = "pref_code"
PREFECTURES_ID = "prefectures_id"
LATITUDE = "latitude"
LONGITUDE = "longitude"


def main(geojson_path: str):
    """メイン処理

    Args:
        geojson_path (str): geojson形式のファイルパス
    """

    # データ読み込み
    with open(geojson_path, encoding="utf-8") as f:
        geojson = json.load(f)
    df = pd.DataFrame(geojson["features"])

    # 整形
    df = processing_after_loading_land_price(
        df, [SYOZAI_CHIBAN_RAW, LAND_PRICE_RAW, NENDO_RAW, JUKYO_HYOJI_RAW]
    )

    # 所在と地番を分割
    df = split_syozai_for_land_price(df)

    # 都道府県データのマージ
    df = add_pref_code_df(df)

    # カラム名の変更
    df = df.rename(
        columns={
            NENDO_RAW: NENDO,
            LAND_PRICE_RAW: LAND_PRICE,
            JUKYO_HYOJI_RAW: JUKYO_HYOJI,
            PREF_CODE: PREFECTURES_ID,
        }
    )

    # 欠損値除去など最終調整
    df.replace([np.nan], [None], inplace=True)
    df.fillna(
        {
            SYOZAI: "",
            CHIBAN: "",
            LAND_PRICE: "",
            NENDO: "",
            JUKYO_HYOJI: "",
            LATITUDE: "",
            LONGITUDE: "",
            PREFECTURES_ID: "",
        },
        inplace=True,
    )

    # DBへ登録
    bulk_create_land_price(df)


def processing_after_loading_land_price(
    df: pd.DataFrame, properties_columns: list
) -> pd.DataFrame:
    """dict型で格納されているデータフレームの要素を展開し加工

    Args:
        df (pd.DataFrame): 未加工のデータフレーム
        properties_columns (list): 最低限必要なカラム名のリスト

    Returns:
        pd.DataFrame: 加工済み公示価格データ
    """
    # 公示価格詳細データを展開
    df_properties = json_normalize(df["properties"].apply(lambda x: x))
    df_properties = df_properties[properties_columns]

    # 緯度経度データを展開
    df_geometry = json_normalize(df["geometry"].apply(lambda x: x))
    df_geometry = df_geometry["coordinates"].apply(pd.Series)
    df_geometry.columns = [LONGITUDE, LATITUDE]

    # 元データと緯度経度のデータをマージ
    df = pd.concat([df_properties, df_geometry], axis=1)

    # 全角を半角に変換
    df[SYOZAI_CHIBAN_RAW] = df[SYOZAI_CHIBAN_RAW].apply(
        lambda x: unicodedata.normalize("NFKC", x)
    )
    df[JUKYO_HYOJI_RAW] = df[JUKYO_HYOJI_RAW].apply(
        lambda x: unicodedata.normalize("NFKC", x)
    )

    # 住居表示からアンダーバーを除去
    df[JUKYO_HYOJI_RAW].replace(["_"], [""], inplace=True)

    return df


def split_syozai_for_land_price(df: pd.DataFrame) -> pd.DataFrame:
    """都道府県, 所在, 地番にデータを分割する"""

    # 都道府県のみ分離（公示価格データは都道府県だけスペースで区切られている）
    df_land_split = df[SYOZAI_CHIBAN_RAW].str.split(" ", expand=True)
    df_land_split = df_land_split.rename(columns={0: TODOFUKEN, 1: SYOZAI_CHIBAN})
    df = df.drop(SYOZAI_CHIBAN_RAW, axis=1)
    df = pd.concat([df, df_land_split], axis=1)

    def split_location_support(split_list: list, untreated_location: str) -> list:
        """分割できなかった場合のサポート処理"""
        if len(split_list) == 1:
            # **番以降とそれ以前にある数字以外の文字以前を分割
            split_list = re.split(r"(.\D?)(?=[\d+]番)", untreated_location)
            if not split_list[1].isdigit():
                chiban = "".join(split_list[2:])
                split_list[0] = "".join(split_list[:2])
            else:
                chiban = "".join(split_list[1:])

            # 所在の最後尾に数値があるとき、地番と結合させる
            while split_list[0][-1].isdigit():
                chiban = split_list[0][-1] + chiban
                split_list[0] = split_list[0][:-1]

            split_list = ["", split_list[0], chiban]

        return split_list

    def split_location(untreated_location: str) -> list:
        """分割条件"""
        if "丁目" in untreated_location:
            split_list = re.split(r"(.+?丁目)(?=\d+)", untreated_location)
            split_list = split_location_support(split_list, untreated_location)

        elif "地割" in untreated_location:
            split_list = re.split(r"(.+?地割)(?=\d+)", untreated_location)
            split_list = split_location_support(split_list, untreated_location)
        else:
            split_list = re.split(r"(.+?)(?=\d+)", untreated_location, 1)

        if "号" in split_list[2]:
            split_list = re.split(r"(.+?号)(?=\d+)", untreated_location, 1)
            split_list = split_location_support(split_list, untreated_location)
        else:
            if "線" in split_list[2]:
                split_list = re.split(r"(.+?線)(?=\d+)", untreated_location, 1)
                split_list = split_location_support(split_list, untreated_location)

        if "区" in split_list[2]:
            split_list = re.split(r"(.+?区)(?=\d+)", untreated_location, 1)
            split_list = split_location_support(split_list, untreated_location)

        if "丁" in split_list[2]:
            split_list = re.split(r"(.+?丁)(?=\d+)", untreated_location, 1)
            split_list = split_location_support(split_list, untreated_location)

        if not re.match(r"\d+番(\d+)?(外)?", split_list[2]):
            if "の" in split_list[2]:
                split_list = ["".join(split_list[1:])]
                split_list = re.split(r"(.+?番町)", untreated_location, 1)
            elif "合併" in split_list[2]:
                pass
            elif re.match(r"^\d+$", split_list[2]):
                pass
            else:
                split_list = ["".join(split_list[1:])]
                split_list = split_location_support(split_list, untreated_location)

        return split_list[1:]

    # 所在と地番を分割
    result = df[SYOZAI_CHIBAN].apply(split_location)

    df = df.drop(SYOZAI_CHIBAN, axis=1)
    df_land_price_split = pd.DataFrame(result.to_list(), index=result.index)
    df_land_price_split.columns = [SYOZAI, CHIBAN]

    # 条件に当てはまる文字列にマッチする正規表現
    pattern = r"\d+番(\d+)?(外)?"

    # Seriesの各要素に対して正規表現で検索し、マッチしない要素だけ抽出する
    result = df_land_price_split[~df_land_price_split[CHIBAN].str.match(pattern)]

    # 最後の文字が番外で終わる文字列の削除
    df_land_price_split[CHIBAN] = df_land_price_split[CHIBAN].apply(
        lambda x: x.replace("番外", "")
    )

    # 番地をハイフンに変換
    df_land_price_split[CHIBAN] = df_land_price_split[CHIBAN].apply(
        lambda x: x.replace("番", "-")
    )
    # 最後にハイフンで終わる文字列のハイフン削除（最後に番地または番外地で終わる場合）
    df_land_price_split[CHIBAN] = df_land_price_split[CHIBAN].apply(
        lambda x: x[:-1] if x[-1] in ("-", "外", "内") else x
    )
    # 元データにマージ
    df = pd.concat([df, df_land_price_split], axis=1)

    return df


def add_pref_code_df(df: pd.DataFrame) -> pd.DataFrame:
    """都道府県コードを付与"""
    PREFECTURES_NANE = "name"
    df_city = read_frame(Prefectures.objects.all())

    df = pd.merge(
        df,
        df_city[[PREFECTURES_NANE, PREF_CODE]],
        left_on=TODOFUKEN,
        right_on=PREFECTURES_NANE,
        how="left",
    ).drop([TODOFUKEN, PREFECTURES_NANE], axis=1)
    df[PREF_CODE] = df[PREF_CODE].astype(int)
    return df


def bulk_create_land_price(in_df: pd.DataFrame):
    # pylint: disable=W0719
    """DBへ登録"""
    land_price_for_insert = [
        PublicLandPrice(**row) for row in in_df.to_dict(orient="records")
    ]

    # 未登録データが登録済みでないかの確認
    q_filter = Q()
    for insert_row in land_price_for_insert:
        q_filter = (
            Q(year=insert_row.year)
            & Q(location=insert_row.location)
            & Q(chiban=insert_row.chiban)
        )
        duplicate_list = PublicLandPrice.objects.filter(q_filter)

    if not duplicate_list.exists():
        PublicLandPrice.objects.bulk_create(land_price_for_insert)
    else:
        raise Exception("データ登録済みエラー")
