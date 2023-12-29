from typing import TypedDict


class RequestType(TypedDict):
    pref_codes: str


class EncodedRequestType(TypedDict):
    pref_codes: list[str]


class CityResponseType(TypedDict):
    id: int
    name: str
    city_code: str


class ResponseType(TypedDict):
    list: list[CityResponseType]
