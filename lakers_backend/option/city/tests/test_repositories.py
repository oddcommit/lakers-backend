from django.test import TestCase

from lakers_backend.option.city.repositories import CityReader
from lakers_backend.option.city.tests.factory import PrefecturesCityFactory
from lakers_backend.option.city.types import EncodedRequestType


class CityReaderTest(TestCase):
    def setUp(self):
        self.repository = CityReader()
        self.prefectures_city_factory = PrefecturesCityFactory()

    def test__read__不明を除いた東京都の市区町村が取得できること(self):
        # Arrange
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()
        request_type = EncodedRequestType(pref_codes=["13"])

        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)

        # Assert
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, "東京都新宿区")

    def test__read__不明を除いた神奈川県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()

        request_type = EncodedRequestType(pref_codes=["14"])
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, "横浜市青葉区")

    def test__read__不明を除いた埼玉県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()

        request_type = EncodedRequestType(pref_codes=["11"])

        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, "さいたま市大宮区")

    def test__read__不明を除いた千葉県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()
        request_type = EncodedRequestType(pref_codes=["12"])

        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, "千葉市稲毛区")

    def test__read__不明を除いた2県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()

        request_type = EncodedRequestType(pref_codes=["12", "13"])

        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].name, "東京都新宿区")
        self.assertEqual(actual[1].name, "千葉市稲毛区")

    def test__read__不明を除いた3県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()

        request_type = EncodedRequestType(pref_codes=["11", "12", "13"])
        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)
        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0].name, "東京都新宿区")
        self.assertEqual(actual[1].name, "さいたま市大宮区")
        self.assertEqual(actual[2].name, "千葉市稲毛区")

    def test__read__不明を除いた4県の市区町村が取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()

        request_type = EncodedRequestType(pref_codes=["11", "12", "13", "14"])
        # Act
        actual = self.repository.read(user_id=0, is_superuser=True, data=request_type)
        self.assertEqual(len(actual), 4)
        self.assertEqual(actual[0].name, "東京都新宿区")
        self.assertEqual(actual[1].name, "横浜市青葉区")
        self.assertEqual(actual[2].name, "さいたま市大宮区")
        self.assertEqual(actual[3].name, "千葉市稲毛区")

    def test__read__市区町村コードから都道府県名と都道府県コードを取得できること(self):
        self.prefectures_city_factory.create_prefectures_city()
        self.prefectures_city_factory.create_unknown_prefectures_city()
        actual = self.repository.get_prefecture_name_from_city_code("1")
        self.assertEqual(actual, "東京都")
