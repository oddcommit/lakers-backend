from typing import List, TypedDict


class RequestType(TypedDict):
    user_id: str


class PrefectureResponseType(TypedDict):
    id: int
    name: str
    prefecture_code: str


class ResponseType(TypedDict):
    list: List[PrefectureResponseType]
