from datetime import datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from data_models.models import ReceptionBookImport, User
from lakers_backend.real_estate_book.views import (
    RealEstateReceptionBookImportStatusView,
)

JST = ZoneInfo("Asia/Tokyo")


class ImportStatus(TypedDict):
    prefectures_id: str
    import_date: str
    request_month: str


class TestRealEstateReceptionBookImportStatusUseCase:
    user: User

    @pytest.fixture
    def prepare_data(self, db):  # pylint: disable=W0613
        self.user = User.objects.create_user(
            email="sample@example.com", password="Password12334556678"
        )

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
    def test_get(self, prepare_data):  # pylint: disable=W0613
        rf = APIRequestFactory()
        request = rf.get("/real_estate_book/import-status")
        view = RealEstateReceptionBookImportStatusView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request)
        assert response.status_code == 200
        actual = response.data
        assert "list" in actual
        assert len(actual["list"]) == 2
        result_list = actual["list"]
        pref13 = result_list[0]
        assert pref13["prefectures_id"] == 13
        assert pref13["prefectures_name"] == "東京都"
        assert pref13["import_date"] == "2023-07-13"
        assert pref13["legal_affairs_bureau_request_month"] == "2023-06"
        pref12 = result_list[1]
        assert pref12["prefectures_id"] == 12
        assert pref12["prefectures_name"] == "千葉県"
        assert pref12["import_date"] == "2023-05-11"
        assert pref12["legal_affairs_bureau_request_month"] == "2023-04"
