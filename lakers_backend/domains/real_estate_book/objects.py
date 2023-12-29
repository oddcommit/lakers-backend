import datetime
from dataclasses import dataclass
from typing import Optional


class DReceptionReason:
    def __init__(self, id: int, name: str):  # pylint: disable=redefined-builtin
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class DRealEstateReceptionBook:
    def __init__(
        self,
        id: int,  # pylint: disable=redefined-builtin
        chiban: str,
        kaoku_number: str,
        real_estate_book_type_id: Optional[int],
        real_estate_book_type_name: str,
        reception_reason: str,
        real_estate_type_id: Optional[int],
        real_estate_type_name: str,
        is_new: bool,
        prefectures_city_id: int,
        city_id: int,
        city_name: str,
        prefectures_id: int,
        prefectures_name: str,
        address: str,
        outside: Optional[int],
        legal_affairs_bureau_request_date: Optional[datetime.date],
        legal_affairs_bureau_reception_number: Optional[str],
    ):
        self._id = id
        self._chiban = chiban
        self._kaoku_number = kaoku_number
        self._real_estate_book_type_id = real_estate_book_type_id
        self._real_estate_book_type_name = real_estate_book_type_name
        self._reception_reason = reception_reason
        self._real_estate_type_id = real_estate_type_id
        self._real_estate_type_name = real_estate_type_name
        self._is_new = is_new
        self._prefectures_city_id = prefectures_city_id
        self._city_id = city_id
        self._city_name = city_name
        self._prefectures_id = prefectures_id
        self._prefectures_name = prefectures_name
        self._address = address
        self._outside = outside
        self._legal_affairs_bureau_request_date = legal_affairs_bureau_request_date
        self._legal_affairs_bureau_reception_number = (
            legal_affairs_bureau_reception_number
        )

    @property
    def id(self):
        return self._id

    @property
    def chiban(self):
        return self._chiban

    @property
    def kaoku_number(self):
        return self._kaoku_number

    @property
    def real_estate_book_type_id(self):
        return self._real_estate_book_type_id

    @property
    def real_estate_book_type_name(self):
        return self._real_estate_book_type_name

    @property
    def reception_reason(self):
        return self._reception_reason

    @property
    def real_estate_type_id(self):
        return self._real_estate_type_id

    @property
    def real_estate_type_name(self):
        return self._real_estate_type_name

    @property
    def is_new(self):
        return self._is_new

    @property
    def prefectures_city_id(self):
        return self._prefectures_city_id

    @property
    def city_id(self):
        return self._city_id

    @property
    def city_name(self):
        return self._city_name

    @property
    def prefectures_id(self):
        return self._prefectures_id

    @property
    def prefectures_name(self):
        return self._prefectures_name

    @property
    def address(self):
        return self._address

    @property
    def outside(self):
        return self._outside

    @property
    def legal_affairs_bureau_request_date(self):
        return self._legal_affairs_bureau_request_date

    @property
    def legal_affairs_bureau_reception_number(self):
        return self._legal_affairs_bureau_reception_number


@dataclass(frozen=True)
class DUserPlan:
    id: int
    plan_id: int
    prefecture_code: str
    city_code: str
    plan_type: str
