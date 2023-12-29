from abc import ABC, abstractmethod
from typing import TypeVar

from .objects import DPrefecture

T = TypeVar("T")


class IPrefectureReader(ABC):
    @abstractmethod
    def read(self, user_id: int, is_superuser: bool) -> list[DPrefecture]:
        raise NotImplementedError()

    @abstractmethod
    def get_prefecture_ids(self, user_id: int) -> list[str]:
        raise NotImplementedError()
