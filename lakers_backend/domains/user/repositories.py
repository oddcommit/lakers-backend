from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class IUserReader(ABC):
    @abstractmethod
    def is_super_user(self, user_id: int) -> bool:
        raise NotImplementedError()
