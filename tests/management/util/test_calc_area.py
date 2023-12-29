import logging

from common_calc import calc_assert_raw
from factory import ChisekiDataFrameFactory

from lakers_backend.management.commands.util.calc_area import apply_calc_area

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
chiseki_dataframe_builder = ChisekiDataFrameFactory()


def test_apply_calc_area_tokyo_public_and_arbitrarily_coord_systems():
    """
    東京：公共座標9系と任意座標系の混在
    """
    _input_df = chiseki_dataframe_builder.tokyo_data
    result_df = apply_calc_area(_input_df, "東京都")
    calc_assert_raw(result_df)


def test_apply_calc_area_okinawa_only_public_coord_systems():
    """
    沖縄：公共座標系のみ
    """
    _input_df = chiseki_dataframe_builder.okinawa_only_public
    result_df = apply_calc_area(_input_df, "沖縄県")
    calc_assert_raw(result_df)


def test_apply_calc_area_hokkaido_multi_public_coord_systems():
    """
    北海道：公共座標系混在
    混在していてもエラーにならない
    """
    _input_df = chiseki_dataframe_builder.hokkaido_multi_public
    result_df = apply_calc_area(_input_df, "北海道")
    calc_assert_raw(result_df)
