import logging
import os
import pathlib
from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pandera as pa
from django_pandas.io import read_frame

from data_models.models import (
    PrefecturesCity,
    RealEstateReceptionBook,
    ReceptionBookImport,
)

logger = logging.getLogger(__name__)

JST = ZoneInfo("Asia/Tokyo")
FINAL_COLS = [
    "chiban",
    "kaoku_number",
    "reception_reason",
    "is_new",
    "address",
    "outside",
    "legal_affairs_bureau_request_date",
    "legal_affairs_bureau_reception_number",
    "prefectures_city_id",
    "real_estate_book_type_id",
    "real_estate_type_id",
]


def get_schema() -> pa.DataFrameSchema:
    schema_cols_map = {
        "outside": pa.Column(
            str, pa.Check(lambda s: s.str.isdecimal(), name="is_decimal"), nullable=True
        )
    }
    model_meta = RealEstateReceptionBook._meta
    for model_field_name in FINAL_COLS:
        if (field := model_meta.get_field(model_field_name)) and (
            max_length := field.max_length
        ):
            schema_cols_map[model_field_name] = pa.Column(
                str, pa.Check.str_length(max_value=max_length), nullable=True
            )

    return pa.DataFrameSchema(schema_cols_map)


@lru_cache
def current_time() -> datetime:
    return datetime.now(JST)


def get_output_dir_base():
    return os.getenv("LAKERS_OUTPUTS_BASE", "local_work")


def real_estate_reception_book_type(text: str) -> int | None:
    if text == "連先":
        return 1
    elif text == "連続":
        return 2
    elif text == "単独":
        return 3
    else:
        return None


def real_estate_type(text: str) -> int | None:
    if text == "建物":
        return 1
    elif text == "土地":
        return 2
    elif text == "区建":
        return 3
    elif text == "共担":
        return 4
    elif text == "その他":
        return 5
    elif text == "一棟":
        return 6
    else:
        return None


def is_new(text: str) -> bool:
    return text == "新"


def create_pref_city_df(prefecture):
    df = read_frame(
        PrefecturesCity.objects.filter(prefectures__name=prefecture),
        fieldnames=["city__name", "prefectures__name", "prefectures__id", "id"],
    )
    return df.rename(
        columns={
            "city__name": "市区町村",
            "prefectures__name": "都道府県",
            "prefectures__id": "pref_id",
            "id": "共通ID",
        }
    )


def apply_ymd_jp_format(text: str, year: int):
    """
    text: ○月○日形式
    """
    return f"{year}年{text}"


def apply_ymd_yyyy_mm_dd(text: str):
    """
    text: YYYY-MM-DD形式: a.g 2023-07-01
    """
    y, m, d = text.split("-")
    return f"{y}年{m}月{d}日"


def main(raw_csv_path: str, prefecture: str, year: int | None):
    df = pd.read_csv(raw_csv_path, dtype={"法務局受付番号": str, "外": str})

    # もし不動産種別が土地以外の場合は、家屋番号列に入れる
    df["家屋番号"] = df[(df["不動産種別"] != "土地")]["地番または家屋番号"]
    df["地番"] = df[(df["不動産種別"] == "土地")]["地番または家屋番号"]

    df["法務局受付日"] = df["法務局受付日"].replace("*", None)
    df["法務局受付日"] = df["法務局受付日"].fillna(method="ffill")
    first_row = df.iloc[0]
    if "月" in first_row["法務局受付日"]:
        if year is not None:
            df["年月日"] = df["法務局受付日"].apply(apply_ymd_jp_format, year=year)
        else:
            raise ValueError("引数yearは必須です")
    else:
        df["年月日"] = df["法務局受付日"].apply(apply_ymd_yyyy_mm_dd)
    df["年月日"] = pd.to_datetime(df["年月日"], format="%Y年%m月%d日", errors="coerce")

    df_city = create_pref_city_df(prefecture)

    pattern = "|".join(df_city["市区町村"])
    df["市区町村"] = df["所在"].str.extract(f"({pattern})")
    df = pd.merge(df, df_city, how="left", on="市区町村")

    df["都道府県"] = df["都道府県"].fillna(method="ffill")

    df["不動産種別"] = df["不動産種別"].apply(real_estate_type)
    df["申請種別"] = df["申請種別"].apply(real_estate_reception_book_type)
    df["新・既"] = df["新・既"].apply(is_new)
    df["市区町村"] = df["市区町村"].fillna("不明")

    df["外"] = df["外"].replace("-", None)

    df = pd.merge(df, df_city, how="left", on=["市区町村", "都道府県"])
    df = df[
        [
            "法務局受付番号",
            "年月日",
            "申請種別",
            "登記原因",
            "新・既",
            "不動産種別",
            "所在",
            "外",
            "家屋番号",
            "地番",
            "共通ID_y",
            "pref_id_y",
        ]
    ]

    df = df.rename(
        columns={
            "法務局受付番号": "legal_affairs_bureau_reception_number",
            "年月日": "legal_affairs_bureau_request_date",
            "申請種別": "real_estate_book_type_id",
            "登記原因": "reception_reason",
            "新・既": "is_new",
            "不動産種別": "real_estate_type_id",
            "所在": "address",
            "外": "outside",
            "家屋番号": "kaoku_number",
            "地番": "chiban",
            "共通ID_y": "prefectures_city_id",
            "pref_id_y": "pref_id",
        }
    )
    output_result_csv(raw_csv_path, df, "converted", cols=FINAL_COLS)
    try:
        get_schema().validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        fail_index = err.failure_cases["index"]
        if len(fail_index) > 0:
            fail_cases_df = err.failure_cases[
                ["index", "column", "check", "failure_case"]
            ]
            output_result_csv(raw_csv_path, fail_cases_df, "failed_causes")
            output_result_csv(
                raw_csv_path, df[df.index.isin(fail_index)], "failed", cols=FINAL_COLS
            )
            logger.exception("Schema error occurred.")
            df = df[~df.index.isin(fail_index)]  # 成功したものだけ残す。 `~`で反転させる
    bulk_create_books(df)
    update_import_status(df[["pref_id", "legal_affairs_bureau_request_date"]])


def output_result_csv(raw_csv_path, df: pd.DataFrame, label: str, cols: list = None):
    current = current_time()
    raw_csv_path_obj = pathlib.Path(raw_csv_path)
    if cols:
        df = df[FINAL_COLS]
    df.to_csv(
        f"./{get_output_dir_base()}/{current.strftime('%Y%m%d-%H%M%S')}_{label}_{raw_csv_path_obj.stem}.csv",
        index=False,
    )


def bulk_create_books(in_df: pd.DataFrame):
    in_df.replace([np.nan], [None], inplace=True)
    in_df.fillna(
        {
            "chiban": "",
            "kaoku_number": "",
            "reception_reason": "",
            "address": "",
            "legal_affairs_bureau_reception_number": "",
        },
        inplace=True,
    )
    books_for_insert = []
    for row in in_df.to_dict(orient="records"):
        del row["pref_id"]
        books_for_insert.append(RealEstateReceptionBook(**row))
    RealEstateReceptionBook.objects.bulk_create(books_for_insert)


def update_import_status(in_df: pd.DataFrame):
    grouped_df = in_df.groupby("pref_id").max()
    now = current_time()
    for row in grouped_df.itertuples():
        request_date: pd.Timestamp = row.legal_affairs_bureau_request_date
        request_date_day1 = datetime(
            year=request_date.year, month=request_date.month, day=1
        )
        ReceptionBookImport.objects.create(
            prefectures_id=row.Index,
            import_date=now.date(),
            legal_affairs_bureau_request_month=request_date_day1,
        )
