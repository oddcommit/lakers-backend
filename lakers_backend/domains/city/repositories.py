from abc import abstractmethod
from typing import Generic, List, TypeVar

from .objects import DCity

T = TypeVar("T")


class ICityReader(Generic[T]):
    @abstractmethod
    def read(self, user_id: int, is_superuser: bool, data: T) -> List[DCity]:
        raise NotImplementedError()

    @abstractmethod
    def get_normal_city_user_ids(self, user_id: int, data: T) -> list[str]:
        raise NotImplementedError()
