from django.test import TestCase

from lakers_backend.management.commands.data_input.geojson import load_geojson
from lakers_backend.management.commands.data_input.load_chiseki_map import (
    build_df_with_prefecture_name,
    build_prefecture_info_to_df,
    calc_chiseki,
    load_dataloader,
    load_jsonl,
)
from tests.management.util.common_calc import calc_assert_raw
from tests.management.util.factory import ChisekiDataFrameFactory


class LoadChisekiTest(TestCase):
    def test__jsonlで呼び出されるように指定するとjsonlで読み込み関数が呼ばれる(self):
        result = load_dataloader(True)
        self.assertEqual(result, load_jsonl)

    def test__jsonl意外で呼び出されるように指定するとjsonで読み込み関数が呼ばれる(self):
        result = load_dataloader(False)
        self.assertEqual(result, load_geojson)

    def test__東京都の市区町村が格納されているデータからを算出できる(self):
        tokyo_dataset = ChisekiDataFrameFactory().tokyo_data
        results_tokyo = build_prefecture_info_to_df(tokyo_dataset)
        for result in results_tokyo:
            self.assertEqual(result, "東京都")

    def test__沖縄県の市区町村が格納されているデータからを算出できる(self):
        okinawa_dataset = ChisekiDataFrameFactory().okinawa_only_public
        results_okinawa = build_prefecture_info_to_df(okinawa_dataset)
        for result in results_okinawa:
            self.assertEqual(result, "沖縄県")

    def test__北海道の市区町村が格納されているデータからを算出できる(self):
        hokkaido_dataset = ChisekiDataFrameFactory().hokkaido_multi_public
        results_hokkaido = build_prefecture_info_to_df(hokkaido_dataset)
        for result in results_hokkaido:
            self.assertEqual(result, "北海道")

    def test__東京都が付与されたデータフレームが生成される(self):
        tokyo_dataset = ChisekiDataFrameFactory().tokyo_data
        results_tokyo = build_df_with_prefecture_name(tokyo_dataset)
        for _, result in results_tokyo.iterrows():
            self.assertEqual(result.都道府県名, "東京都")

    def test__沖縄県が付与されたデータフレームが生成される(self):
        okinawa_dataset = ChisekiDataFrameFactory().okinawa_only_public
        results_okinawa = build_df_with_prefecture_name(okinawa_dataset)
        for _, result in results_okinawa.iterrows():
            self.assertEqual(result.都道府県名, "沖縄県")

    def test__北海道が付与されたデータフレームが生成される(self):
        hokkaido_dataset = ChisekiDataFrameFactory().hokkaido_multi_public
        results_hokkaido = build_df_with_prefecture_name(hokkaido_dataset)
        for _, result in results_hokkaido.iterrows():
            self.assertEqual(result.都道府県名, "北海道")

    def test__東京都が付与されたデータフレームから地積を算出できる(self):
        tokyo_dataset = ChisekiDataFrameFactory().tokyo_data
        results_tokyo = build_df_with_prefecture_name(tokyo_dataset)
        result_df = calc_chiseki(results_tokyo)
        calc_assert_raw(result_df)

    def test__沖縄県が付与されたデータフレームから地積を算出できる(self):
        okinawa_dataset = ChisekiDataFrameFactory().okinawa_only_public
        results_okinawa = build_df_with_prefecture_name(okinawa_dataset)
        result_df = calc_chiseki(results_okinawa)
        calc_assert_raw(result_df)

    def test__北海道が付与されたデータフレームから地積を算出できる(self):
        hokkaido_dataset = ChisekiDataFrameFactory().hokkaido_multi_public
        results_hokkaido = build_df_with_prefecture_name(hokkaido_dataset)
        result_df = calc_chiseki(results_hokkaido)
        calc_assert_raw(result_df)
