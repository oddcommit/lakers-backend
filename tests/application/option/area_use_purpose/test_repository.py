from django.test import TestCase

from data_models.models import AreaUsePurposeType
from lakers_backend.option.area_use_purpose.repositories import (
    AreaUsePurposeConditions,
    AreaUsePurposeReader,
)

from .factory import AreaUsePurposeFactory


class AreaUsePurposeTest(TestCase):
    def setUp(self):
        AreaUsePurposeFactory.build_area_use_purpose_conditions()

    def test__存在しないデータの用途地域種別テーブルからデータを取得しようとした場合データを投入した上で取得する(self):
        self.assertEqual(AreaUsePurposeType.objects.count(), 12)
        result = AreaUsePurposeReader.get_or_create_use_purpose_type("13", "test")
        self.assertEqual(result.area_use_purpose_type, "13")
        self.assertEqual(result.name, "test")
        self.assertEqual(AreaUsePurposeType.objects.count(), 13)

    def test__存在するデータを指定した場合対象となるデータを取得するデータ数は増えない(self):
        AreaUsePurposeReader.get_or_create_use_purpose_type("1", "第一種低層住居専用地域")
        result = AreaUsePurposeReader.get_or_create_use_purpose_type("1", "第一種低層住居専用地域")
        self.assertEqual(result.area_use_purpose_type, "1")
        self.assertEqual(result.name, "第一種低層住居専用地域")
        self.assertEqual(AreaUsePurposeType.objects.count(), 12)

    def test__対象となる都道府県と市区町村コードで正常に存在するデータはデータを取得できる(self):
        target_prefecture = "東京都"
        target_city_code = "13210"
        result = AreaUsePurposeReader.get_area_use_purpose_conditions(
            target_prefecture, target_city_code
        )
        self.assertEqual(result.prefecture_city.prefectures.name, target_prefecture)
        self.assertEqual(result.prefecture_city.city.name, "小金井市")
        self.assertEqual(result.miniature, 10000)
        self.assertEqual(result.publish_flag, 1)

    def test__対象となる都道府県と市区町村コードで存在しないデータは例外になる(self):
        target_prefecture = "東京都"
        target_city_code = "23210"
        with self.assertRaises(AreaUsePurposeConditions.DoesNotExist):
            AreaUsePurposeReader.get_area_use_purpose_conditions(
                target_prefecture, target_city_code
            )

    def test__対象となる都道府県と市区町村コードで存在しないデータで取得しようとすると一件もデータを取得できない(self):
        AreaUsePurposeFactory().init_area_use_purpose(
            has_initialized_purpose_conditions=True,
            has_initialized_use_purpose_type=False,
        )
        target_prefecture = "静岡県"
        target_city_code = "22202"
        result = AreaUsePurposeReader.get_area_use_purpose(
            target_prefecture, target_city_code
        )
        self.assertEqual(len(result), 0)

    def test__対象となる都道府県と市区町村コードで存在するで取得しようとするとデータを取得できる(self):
        AreaUsePurposeFactory().init_area_use_purpose(
            has_initialized_purpose_conditions=True,
            has_initialized_use_purpose_type=False,
        )
        target_prefecture = "東京都"
        target_city_code = "13201"
        result = AreaUsePurposeReader.get_area_use_purpose(
            target_prefecture, target_city_code
        )
        self.assertTrue(len(result) > 0)
