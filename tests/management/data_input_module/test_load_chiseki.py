from django.test import TestCase

from lakers_backend.management.commands.data_input.load_chiseki_map import (
    load_all_properties,
    load_raw_dataset_with_prefectures_info,
)


class LoadChisekiTestCase(TestCase):
    def test__PrefectureCityに登録されていない市区町村が取り除かれた結果を取得する(self):
        target_dir = "tests/management/data_input_module/data/chiseki_jsonls"
        result = load_raw_dataset_with_prefectures_info(target_dir, True)
        self.assertEqual(len(result), 2)

    def test__PrefectureCityに登録されていない市区町村が取り除かれた地積を取得する(self):
        target_dir = "tests/management/data_input_module/data/chiseki_jsonls"
        result = load_all_properties(target_dir, True)
        self.assertEqual(result.都道府県名.to_list(), ["静岡県", "静岡県"])
