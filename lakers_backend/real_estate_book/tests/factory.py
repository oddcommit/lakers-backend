import datetime
from typing import Optional

from data_models.models import RealEstateReceptionBook


class RealEstateReceptionBookFactory:
    def create_real_estate_book_data(
        self,
        prefectures_city_id: int,
        legal_affairs_bureau_request_date: Optional[
            datetime.date
        ] = datetime.date.today(),
        reception_reason: str = "登記原因",
    ):
        return RealEstateReceptionBook.objects.create(
            chiban="地番",
            kaoku_number="家屋番号",
            real_estate_book_type_id=None,
            reception_reason=reception_reason,
            real_estate_type_id=None,
            is_new=True,
            prefectures_city_id=prefectures_city_id,
            address="住所",
            outside=1,
            legal_affairs_bureau_request_date=legal_affairs_bureau_request_date,
            legal_affairs_bureau_reception_number="法務局受付番号",
        )

    # id以外同じデータをcount分bulk_createする
    def bulk_create_real_estate_book_today_data(
        self, prefectures_city_id: int, size: int
    ):
        data = []
        for _ in range(size):
            data.append(
                RealEstateReceptionBook(
                    chiban="地番",
                    kaoku_number="家屋番号",
                    real_estate_book_type_id=None,
                    reception_reason="登記原因",
                    real_estate_type_id=None,
                    is_new=True,
                    prefectures_city_id=prefectures_city_id,
                    address="住所",
                    outside=1,
                    legal_affairs_bureau_request_date=datetime.date.today(),
                    legal_affairs_bureau_reception_number="法務局受付番号",
                )
            )
        return RealEstateReceptionBook.objects.bulk_create(data)

    def bulk_create_real_estate_book_today_dataset(
        self, prefectures_city_ids: list[int], size: int
    ):
        return [
            self.bulk_create_real_estate_book_today_data(prefectures_city_id, size)
            for prefectures_city_id in prefectures_city_ids
        ]
