from typing import Generic, List, TypeVar

from .objects import DCity
from .repositories import ICityReader

T = TypeVar("T")


class CityService(Generic[T]):
    def __init__(self, reader: ICityReader, user_id: int, is_superuser: bool, data: T):
        self._reader = reader
        self._data = data
        self._user_id = user_id
        self._is_superuser = is_superuser

    def execute(self) -> List[DCity]:
        domain_list = self._reader.read(
            user_id=self._user_id, data=self._data, is_superuser=self._is_superuser
        )
        return domain_list

    def get_normal_city_user_ids(self) -> list[str]:
        city_ids = self._reader.get_normal_city_user_ids(
            user_id=self._user_id, data=self._data
        )
        return city_ids
