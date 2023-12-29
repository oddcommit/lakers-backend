from datetime import date, datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

import pytest

from data_models.models import ReceptionBookImport
from lakers_backend.real_estate_book.repositories import ReceptionBookImportReader

JST = ZoneInfo("Asia/Tokyo")


class ImportStatus(TypedDict):
    prefectures_id: str
    import_date: str
    request_month: str


class TestReceptionBookImportReader:
    repository = ReceptionBookImportReader()

    @pytest.fixture
    def prepare_data(self, db):  # pylint: disable=W0613
        import_statuses: list[ImportStatus] = [
            ImportStatus(
                prefectures_id="13",
                request_month="2023-06-01",
                import_date="2023-07-13",
            ),
            ImportStatus(
                prefectures_id="13",
                request_month="2023-05-01",
                import_date="2023-06-12",
            ),
            ImportStatus(
                prefectures_id="12",
                request_month="2023-04-01",
                import_date="2023-05-11",
            ),
            ImportStatus(
                prefectures_id="12",
                request_month="2023-03-01",
                import_date="2023-04-10",
            ),
        ]
        for status in import_statuses:
            import_date = datetime.strptime(status["import_date"], "%Y-%m-%d").replace(
                tzinfo=JST
            )
            request_month = datetime.strptime(
                status["request_month"], "%Y-%m-%d"
            ).replace(tzinfo=JST)
            ReceptionBookImport.objects.create(
                prefectures_id=status["prefectures_id"],
                import_date=import_date,
                legal_affairs_bureau_request_month=request_month,
            )

    @pytest.mark.django_db
    def test_read(self, prepare_data):  # pylint: disable=W0613
        actual = self.repository.read()
        assert len(actual) == 2
        pref13 = actual[0]
        assert pref13.prefectures_id == "13"
        assert pref13.prefectures_name == "東京都"
        assert pref13.import_date == date(2023, 7, 13)
        assert pref13.legal_affairs_bureau_request_month == date(2023, 6, 1)
        pref12 = actual[1]
        assert pref12.prefectures_id == "12"
        assert pref12.prefectures_name == "千葉県"
        assert pref12.import_date == date(2023, 5, 11)
        assert pref12.legal_affairs_bureau_request_month == date(2023, 4, 1)
