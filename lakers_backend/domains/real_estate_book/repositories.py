from abc import abstractmethod
from typing import Generic, TypeVar

from .objects import DRealEstateReceptionBook, DReceptionReason, DUserPlan

T = TypeVar("T")


class IRealEstateReceptionBookReader(Generic[T]):
    @abstractmethod
    def read(
        self, user_id: int, is_superuser: bool, data: T
    ) -> list[DRealEstateReceptionBook]:
        raise NotImplementedError()

    @abstractmethod
    def count(self, user_id: int, is_superuser: bool, data: T) -> int:
        raise NotImplementedError()


class IReceptionReasonReader(Generic[T]):
    @abstractmethod
    def read(self) -> list[DReceptionReason]:
        raise NotImplementedError()


class IUserPlanRender(Generic[T]):
    def read(self, user_id: int) -> list[DUserPlan]:
        raise NotImplementedError()
