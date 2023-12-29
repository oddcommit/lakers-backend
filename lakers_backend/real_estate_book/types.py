from typing import Optional, TypedDict, Union

# リクエストで必須のパラメータ


class RequestTypeRequired(TypedDict):
    legal_affairs_bureau_request_date_start: str
    legal_affairs_bureau_request_date_end: str
    real_estate_book_type_tandoku: str
    real_estate_book_type_rensaki_renzoku: str
    real_estate_type_tochi: str
    real_estate_type_kutate: str
    real_estate_type_tatemono: str
    real_estate_type_kyotan: str
    cities: list[str]
    prefectures: list[str]
    reception_reasons: list[str]
    sort_by: Optional[str]
    order: Optional[str]
    size: str
    from_count: str


# 必須の型を継承した、任意のパラメータ


class RequestType(RequestTypeRequired, total=False):
    sort_by: str | None
    order: str | None


class RealEstateReceptionBookResponseType(TypedDict):
    id: int
    chiban: str
    kaoku_number: str
    real_estate_book_type_id: Union[None, int]
    real_estate_book_type_name: str
    reception_reason: str
    real_estate_type_id: Union[None, int]
    real_estate_type_name: str
    is_new: bool
    prefectures_city_id: Union[None, int]
    city_id: Union[None, int]
    city_name: str
    prefectures_id: Union[None, int]
    prefectures_name: str
    address: str
    outside: Union[None, int]
    legal_affairs_bureau_request_date: str
    legal_affairs_bureau_reception_number: str


class ResponseType(TypedDict):
    list: list[RealEstateReceptionBookResponseType]
    count: int


class ImportStatusResponse(TypedDict):
    prefectures_id: int
    prefectures_name: str
    import_date: str
    legal_affairs_bureau_request_month: str


class ImportStatusListResponse(TypedDict):
    list: list[ImportStatusResponse]
