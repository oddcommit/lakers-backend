from django.test import TestCase
from shapely.geometry import Point

from lakers_backend.management.commands.data_input.load_area_use_purpose import (
    calc_centroid,
    convert_kokudo_geo_api_result_to_city_code,
    find_within_polygon,
    get_city_code_from_lat_lon,
)
from tests.application.option.area_use_purpose.factory import AreaUsePurposeFactory


class LoadAreaUsePurposeTest(TestCase):
    def setUp(self):
        self.area_use_purpose_conditions = (
            AreaUsePurposeFactory.build_area_use_purpose_conditions()
        )
        self.area_use_purpose_type = AreaUsePurposeFactory.build_area_use_purpose_type()

    def test__ポリゴンの重心が求められる(self):
        polygon = [
            [
                (0, 0),
                (70, 0),
                (70, 25),
                (45, 45),
                (45, 180),
                (95, 188),
                (95, 200),
                (-25, 200),
                (-25, 188),
                (25, 180),
                (25, 45),
                (0, 25),
            ]
        ]
        result = calc_centroid(polygon)
        self.assertEqual(result.x, 35)
        self.assertEqual(result.y, 100.46145124716553)

    def test__東経135度北緯35度の基準点から西脇市の市区町村コードが算出される(self):
        position = Point(135, 35)
        result = get_city_code_from_lat_lon(position)
        self.assertEqual(result, "28213")

    def test__国土地理院APIで結果が空である場合不明のコードを返す(self):
        mock_response = {"muniCd": ""}
        self.assertEqual(
            convert_kokudo_geo_api_result_to_city_code(mock_response), "99999"
        )

    def test__国土地理院APIで結果の先頭1文字目の値が0の場合4桁のコードになる(self):
        mock_response = {"muniCd": "01101"}
        self.assertEqual(
            convert_kokudo_geo_api_result_to_city_code(mock_response), "1101"
        )

    def test__国土地理院APIで結果の先頭1文字目の値が0ではない場合5桁のコードになる(self):
        mock_response = {"muniCd": "28213"}
        self.assertEqual(
            convert_kokudo_geo_api_result_to_city_code(mock_response), "28213"
        )

    def test__ポリゴン内に存在するデータは対象となるデータを返す(self):
        polygon = [[[5, 5], [10, 5], [10, 10], [5, 10]]]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(7, 8, [target_param])

        self.assertEqual(result, target_param)

    def test__ポリゴン内に存在しないデータはNullを返す(self):
        polygon = [[[5, 5], [10, 5], [10, 10], [5, 10]]]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(200, 100, [target_param])

        self.assertIsNone(result)

    def test__穴空きポリゴン内に存在するデータは対象となるデータを返す(self):
        polygon = [
            [[5, 5], [10, 5], [10, 10], [5, 10]],
            [[1, 1], [2, 1], [2, 2], [1, 2]],
        ]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(7, 8, [target_param])

        self.assertEqual(result, target_param)

    def test__穴空きポリゴン内の穴空き部存在するデータはNullを返す(self):
        polygon = [
            [[5, 5], [10, 5], [10, 10], [5, 10]],
            [[1, 1], [2, 1], [2, 2], [1, 2]],
        ]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(7 / 5, 8 / 5, [target_param])

        self.assertIsNone(result)

    def test__マルチポリゴン内1個目に存在するデータは対象となるデータを返す(self):
        polygon = [
            [[[5, 5], [10, 5], [10, 10], [5, 10]]],
            [[[20, 20], [40, 20], [40, 40], [20, 40]]],
        ]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(7, 8, [target_param])

        self.assertEqual(result, target_param)

    def test__マルチポリゴン内2個目に存在するデータは対象となるデータを返す(self):
        polygon = [
            [[[5, 5], [10, 5], [10, 10], [5, 10]]],
            [[[20, 20], [40, 20], [40, 40], [20, 40]]],
        ]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(28, 32, [target_param])

        self.assertEqual(result, target_param)

    def test__マルチポリゴン内に存在しないデータはNullを返す(self):
        polygon = [
            [[[5, 5], [10, 5], [10, 10], [5, 10]]],
            [[[20, 20], [40, 20], [40, 40], [20, 40]]],
        ]
        target_param = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_type[0], self.area_use_purpose_conditions[0], polygon
        )
        result = find_within_polygon(5, 20, [target_param])

        self.assertIsNone(result)
