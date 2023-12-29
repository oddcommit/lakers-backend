from datetime import date, datetime

from django.test import TestCase

from lakers_backend.option.city.tests.factory import PrefecturesCityFactory
from lakers_backend.real_estate_book.repositories import RealEstateReceptionBookReader
from lakers_backend.real_estate_book.tests.factory import RealEstateReceptionBookFactory
from lakers_backend.real_estate_book.types import RequestType


class RealEstateReceptionBookReaderTest(TestCase):
    def setUp(self):
        self.repository = RealEstateReceptionBookReader()
        self.prefectures_cities = PrefecturesCityFactory().create_prefectures_city()
        self.unknown_prefectures_city = (
            PrefecturesCityFactory().create_unknown_prefectures_city()
        )
        (
            superuser,
            four_prefecture_user,
            only_tokyo_user,
        ) = PrefecturesCityFactory().create_user_and_plan()
        self.superuser = superuser
        self.four_prefecture_user = four_prefecture_user
        self.only_tokyo_user = only_tokyo_user

    def test__read__sizeの件数分のデータが取得できることスーパーユーザー上限100件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できることスーパーユーザー上限400件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できることスーパーユーザー上限500件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )

        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="500",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できることスーパーユーザー上限500件で東京都のみ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できることスーパーユーザー上限400件で東京都と神奈川県のデータ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 200)

    def test__read__sizeの件数分のデータが取得できること上限400件スーパーユーザーで東京都と神奈川県と千葉県のデータ取得でデータ数は400件(
        self,
    ):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 300)

    def test__read__sizeの件数分のデータが取得できること上限400件スーパーユーザーで一都三県を明示してデータ取得データ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["11", "12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できること一都三県ユーザー上限100件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること一都三県ユーザー上限400件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できること一都三県ユーザー上限500件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )

        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="500",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できること一都三県ユーザー上限500件で東京都のみ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること一都三県ユーザー上限400件で東京都と神奈川県のデータ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 200)

    def test__read__sizeの件数分のデータが取得できること上限400件一都三県ユーザーで東京都と神奈川県と千葉県のデータ取得でデータ数は400件(
        self,
    ):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 300)

    def test__read__sizeの件数分のデータが取得できること上限400件一都三県ユーザーで一都三県を明示してデータ取得データ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["11", "12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.four_prefecture_user.pk,
            self.four_prefecture_user.is_superuser,
            request_type,
        )

        # Assert
        self.assertEqual(len(actual), 400)

    def test__read__sizeの件数分のデータが取得できること東京都のみユーザー上限100件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること東京都のみユーザー上限400件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること東京都のみユーザー上限500件で一都三県でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )

        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="500",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること東京都のみユーザー上限500件で東京都のみ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること東京都のみユーザー上限400件で東京都と神奈川県のデータ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること上限400件東京都のみユーザーで東京都と神奈川県と千葉県のデータ取得でデータ数は400件(
        self,
    ):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__sizeの件数分のデータが取得できること上限400件東京都のみユーザーで東京都以外の三県のデータ取得でデータ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["11", "12", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        with self.assertRaises(ValueError):
            # Act
            self.repository.read(
                self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
            )

    def test__read__sizeの件数分のデータが取得できること上限400件東京都のみユーザーで一都三県を明示してデータ取得データ数は400件(self):
        # Arrange
        RealEstateReceptionBookFactory().bulk_create_real_estate_book_today_dataset(
            prefectures_city_ids=[
                prefectures_cities.pk for prefectures_cities in self.prefectures_cities
            ],
            size=100,
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="1990-01-01",
            legal_affairs_bureau_request_date_end="2200-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=["11", "12", "13", "14"],
            reception_reasons=[],
            size="400",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.only_tokyo_user.pk, self.only_tokyo_user.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 100)

    def test__read__指定区間のデータのみが取得できること(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 2),
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 1)
        self.assertEqual(
            actual[0].legal_affairs_bureau_request_date,
            date(2022, 1, 1),
        )

    def test__read__指定した登記原因のデータが取得できること(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="所有権移転相続・法人合併",
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="取下",
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=["1"],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(actual[0].reception_reason, "所有権移転相続・法人合併")

    def test__read__その他の登記原因のデータが取得できること(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="所有権移転相続・法人合併",
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="選択肢にない登記原因",
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=["999"],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(actual[0].reception_reason, "選択肢にない登記原因")

    def test__read__登記原因が空白のデータは取得されないこと(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="所有権移転相続・法人合併",
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="",
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(actual[0].reception_reason, "所有権移転相続・法人合併")
        self.assertEqual(len(actual), 1)

    def test__read__登記原因が米印のデータは取得されないこと(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="所有権移転相続・法人合併",
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
            reception_reason="*",
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(actual[0].reception_reason, "所有権移転相続・法人合併")
        self.assertEqual(len(actual), 1)

    def test__read__市区町村が不明のデータは取得されないこと(self):
        # Arrange
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.prefectures_cities[0].pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
        )
        RealEstateReceptionBookFactory().create_real_estate_book_data(
            prefectures_city_id=self.unknown_prefectures_city.pk,
            legal_affairs_bureau_request_date=datetime(2022, 1, 1),
        )
        request_type = RequestType(
            legal_affairs_bureau_request_date_start="2022-01-01",
            legal_affairs_bureau_request_date_end="2022-01-01",
            real_estate_book_type_tandoku="false",
            real_estate_book_type_rensaki_renzoku="false",
            real_estate_type_tochi="false",
            real_estate_type_kutate="false",
            real_estate_type_tatemono="false",
            real_estate_type_kyotan="false",
            cities=[],
            prefectures=[],
            reception_reasons=[],
            size="100",
            from_count="0",
        )

        # Act
        actual = self.repository.read(
            self.superuser.pk, self.superuser.is_superuser, request_type
        )

        # Assert
        self.assertEqual(len(actual), 1)
