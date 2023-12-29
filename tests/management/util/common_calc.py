import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def calc_relative_error(calculated_area: float, answer_area: float):
    # 相対誤差の計算
    return abs((calculated_area - answer_area) / answer_area)


def calc_assert_raw(result_df: pd.DataFrame):
    for _i, row in result_df.iterrows():
        area = row["地積"]
        relative_error = calc_relative_error(area, row["面積正解"])
        area_format = "{:.2f}".format(area)
        relative_error_percent = "{:,.2%}".format(relative_error)
        logger.debug(
            f"\n[{row['座標系']}]{row['address']} 地積{area_format}㎡(誤差率: {relative_error_percent})"
        )
        if row["座標系"] == "任意座標系":
            assert relative_error * 100 < 15, "任意座標系の誤差の範囲エラー"  # 誤差15%以内
        else:
            assert relative_error * 100 < 1, "公共座標系の誤差の範囲エラー"  # 誤差1%未満
