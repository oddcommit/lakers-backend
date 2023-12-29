import os

import pandas as pd
import pytest
from django.test import TestCase

from lakers_backend.management.commands.util.run_add_geoinfo import run_add_geoinfo


class RunAddGeoInfoTest(TestCase):
    @pytest.mark.skip
    def test__実行後に生成されるデータに緯度経度の情報が含まれる(self):
        raw_df_path = "tests/management/data/testdata_for_add_geioinfo.pkl"
        output_df_path = "tests/management/data/testdata_for_add_geioinfo_test.pkl"
        run_add_geoinfo(raw_df_path, output_df_path)
        raw_df = pd.read_pickle(raw_df_path)
        add_geoinfo_df = pd.read_pickle(output_df_path)
        for latitude, converted_latitude in zip(
            add_geoinfo_df.query('座標系.str.startswith("公共")')["代表点緯度"].to_list(),
            add_geoinfo_df.query('座標系.str.startswith("公共")')["代表点緯度変換後"].to_list(),
        ):
            self.assertEqual(latitude, converted_latitude)
        for longitude, converted_longitude in zip(
            add_geoinfo_df.query('座標系.str.startswith("公共")')["代表点経度"].to_list(),
            add_geoinfo_df.query('座標系.str.startswith("公共")')["代表点経度変換後"].to_list(),
        ):
            self.assertEqual(longitude, converted_longitude)
        target_syozai_df_base = raw_df[raw_df["所在"] == "小笠原村父島字吹上谷22-3"]
        target_syozai_df_converted = add_geoinfo_df[
            add_geoinfo_df["所在"] == "小笠原村父島字吹上谷22-3"
        ]
        self.assertEqual(
            target_syozai_df_base["代表点経度"].to_list(),
            target_syozai_df_converted["代表点経度変換後"].to_list(),
        )
        self.assertEqual(
            target_syozai_df_base["代表点緯度"].to_list(),
            target_syozai_df_converted["代表点緯度変換後"].to_list(),
        )
        for _, params in add_geoinfo_df.iterrows():
            self.assertTrue(
                params["代表点緯度変換後"] < 90
            )  # 緯度が90より大きくなることはないため緯度経度を間違えて代入していないかの確認
            self.assertTrue(
                params["代表点経度変換後"] > 90
            )  # 日本の国土で経度が90より小さくなることはないため緯度経度を間違えて代入していないかの確認

        os.remove(output_df_path)
