import datetime
from typing import List

from lakers_backend.domains.real_estate_book.objects import DRealEstateReceptionBook


class RealEstateReceptionBookMockDataFactory:
    def generate_feed_mock_data(self, size: int) -> List[DRealEstateReceptionBook]:
        result: List[DRealEstateReceptionBook] = []
        for i in range(size):
            result.append(
                DRealEstateReceptionBook(
                    id=i,
                    chiban=f"chiban{i}",
                    kaoku_number=f"kaoku_number{i}",
                    real_estate_book_type_id=i,
                    real_estate_book_type_name=f"real_estate_book_type_name{i}",
                    reception_reason=f"reception_reason{i}",
                    real_estate_type_id=i,
                    real_estate_type_name=f"real_estate_type_name{i}",
                    is_new=True,
                    prefectures_city_id=i,
                    city_id=i,
                    city_name=f"city_name{i}",
                    prefectures_id=i,
                    prefectures_name=f"prefectures_name{i}",
                    address=f"address{i}",
                    outside=i,
                    legal_affairs_bureau_request_date=datetime.date.today(),
                    legal_affairs_bureau_reception_number=f"法務局受付番号{i}",
                )
            )

        return result
