from dataclasses import dataclass
from typing import Generic, TypeVar

from .objects import DRealEstateReceptionBook, DReceptionReason, DUserPlan
from .repositories import (
    IRealEstateReceptionBookReader,
    IReceptionReasonReader,
    IUserPlanRender,
)

T = TypeVar("T")


class RealEstateReceptionBookFeedService(Generic[T]):
    def __init__(self, reader: IRealEstateReceptionBookReader, data: T):
        self._reader = reader
        self._data = data

    def execute(
        self, user_id: int, is_superuser: bool
    ) -> tuple[list[DRealEstateReceptionBook], int]:
        domain_list = self._reader.read(
            user_id=user_id, is_superuser=is_superuser, data=self._data
        )
        count = self._reader.count(
            user_id=user_id, is_superuser=is_superuser, data=self._data
        )
        return domain_list, count


class ReceptionReasonFeedService(Generic[T]):
    def __init__(self, reader: IReceptionReasonReader):
        self._reader = reader

    def execute(self) -> list[DReceptionReason]:
        return self._reader.read()


@dataclass(frozen=True)
class UserPlanInfoService(Generic[T]):
    reader: IUserPlanRender

    def execute(self, user_id: int) -> list[DUserPlan]:
        return self.reader.read(user_id)
