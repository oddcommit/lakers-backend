from typing import List, TypedDict


class ReceptionReasonResponseType(TypedDict):
    id: int
    name: str


class ResponseType(TypedDict):
    list: List[ReceptionReasonResponseType]
