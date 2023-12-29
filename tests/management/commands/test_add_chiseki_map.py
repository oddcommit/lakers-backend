import math
import os

import pandas as pd
from django.core.management import call_command
from django.test import TestCase


class AddChisekiMapTest(TestCase):
    def test__PrefectureCityに存在する分のデータのみ地積が算出される(self):
        # Arrange
        target_dir = "tests/management/data_input_module/data/chiseki_jsonls"
        output_df = "tests/management/data_input_module/data/tmp"

        # Act
        call_command(
            "add_chiseki_map",
            targetdir=target_dir,
            mode="jsonl",
            dfoutput=output_df,
        )
        result_df_path = (
            "tests/management/data_input_module/data/tmp/chiseki_jsonls.pkl"
        )
        result = pd.read_pickle(result_df_path)
        self.assertEqual(result.都道府県名.to_list(), ["静岡県", "静岡県"])
        for param, calc_result in zip(
            result.地積.to_list(), [220.79505273481834, 133.8748869207439]
        ):
            self.assertTrue(math.isclose(param, calc_result))
        os.remove(result_df_path)
        os.rmdir(output_df)
