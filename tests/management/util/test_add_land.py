from django.test import TestCase
from factory import LandsFactory

from data_models.models import Land, PrefecturesCity
from lakers_backend.management.commands.util.add_land import (
    add_registration_map_and_land,
    create_land,
)


class RunAddLandTest(TestCase):
    def setUp(self):
        self.registration_map = LandsFactory.build_registration_map()

    def test__土地データが作成される(self):
        raw_data = {
            "所在": "東京都新宿区西新宿２丁目8−1",
            "地番": "8−1",
            "代表点緯度変換後": 35.689501,
            "代表点経度変換後": 139.691722,
        }
        prefecture_city = PrefecturesCity.objects.filter(id=658).get()
        result = create_land(raw_data, prefecture_city, self.registration_map[0])
        self.assertEqual(result.location, "東京都新宿区西新宿２丁目")
        self.assertEqual(result.chiban, "8−1")
        self.assertEqual(result.latitude, 35.689501)
        self.assertEqual(result.longitude, 139.691722)

    def test__PrefCityCodeに存在しない箇所の土地データは作成されない(self):
        land_before = Land.objects.count()
        raw_data = {
            "都道府県名": "静岡県",
            "市区町村コード": "22202",  # 旧浜松市のコード
            "所在": "静岡県浜松市中区元城町103-2",
            "地番": "103-2",
            "代表点緯度": 34.7108,
            "代表点経度": 137.7261,
            "地積": 100,
            "coordinates": [[10, 10], [20, 20]],
            "代表点緯度変換後": 34.7108,
            "代表点経度変換後": 137.7261,
            "座標系": "公共座標系",
        }
        self.assertIsNone(add_registration_map_and_land(raw_data))
        land_after = Land.objects.count()
        self.assertEqual(land_before, land_after)

    def test__PrefCityCodeに存在する箇所の土地データは作成される(self):
        land_before = Land.objects.count()
        raw_data = {
            "都道府県名": "静岡県",
            "市区町村コード": "22131",  # 現存する浜松市中区のコード
            "代表点緯度": 34.7108,
            "代表点経度": 137.7261,
            "所在": "静岡県浜松市中区元城町103-2",
            "地番": "103-2",
            "地積": 100,
            "coordinates": [[10, 10], [20, 20]],
            "代表点緯度変換後": 34.7108,
            "代表点経度変換後": 137.7261,
            "座標系": "公共座標系",
        }
        result_land, result_land_area_use_purpose = add_registration_map_and_land(
            raw_data
        )
        self.assertIsNone(result_land_area_use_purpose)  # 静岡県の用途地域データをテストデータには入れていないため
        self.assertEqual(result_land.location, "静岡県浜松市中区元城町")
        self.assertEqual(result_land.chiban, "103-2")
        self.assertEqual(result_land.latitude, 34.7108)
        self.assertEqual(result_land.longitude, 137.7261)
        land_after = Land.objects.count()
        self.assertEqual(land_before + 1, land_after)
