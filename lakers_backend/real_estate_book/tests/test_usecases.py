from unittest import mock

from django.test import TestCase

from lakers_backend.option.city.tests.factory import PrefecturesCityFactory
from lakers_backend.real_estate_book.repositories import RealEstateReceptionBookReader
from lakers_backend.real_estate_book.tests.mock_data_factory import (
    RealEstateReceptionBookMockDataFactory,
)
from lakers_backend.real_estate_book.types import RequestType
from lakers_backend.real_estate_book.usecases import RealEstateReceptionBookFeedUsecase


class RealEstateReceptionBookFeedUsecaseTest(TestCase):
    def setUp(self):
        self.use_case = RealEstateReceptionBookFeedUsecase()

        mock.patch.object(
            RealEstateReceptionBookReader,
            "read",
            return_value=RealEstateReceptionBookMockDataFactory().generate_feed_mock_data(
                5000
            ),
        ).start()
        mock.patch.object(
            RealEstateReceptionBookReader, "count", return_value=10000
        ).start()
        self.users = PrefecturesCityFactory().create_user_and_plan()

    def tearDown(self):
        mock.patch.stopall()

    def test__feed__戻り値の型にlistとcountが含まれていること(self):
        # Arrange
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
            reception_reasons=["13"],
            size="5000",
            from_count="0",
        )

        # Act
        actual = self.use_case.feed(self.users[0].pk, request_type)

        # Assert
        self.assertIn("list", actual)
        self.assertIn("count", actual)

        self.assertEqual(len(actual["list"]), 5000)
        self.assertEqual(actual["count"], 10000)
