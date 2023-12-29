from typing import Generic, TypeVar

from .objects import DPrefecture
from .repositories import IPrefectureReader

T = TypeVar("T")


class PrefectureService(Generic[T]):
    def __init__(self, reader: IPrefectureReader, user_id: int, is_superuser: bool):
        self._reader = reader
        self._user_id = user_id
        self._is_superuser = is_superuser

    def execute(self) -> list[DPrefecture]:
        domain_list = self._reader.read(
            user_id=self._user_id, is_superuser=self._is_superuser
        )
        return domain_list

    def get_prefecture_ids(self) -> list[str]:
        id_list = self._reader.get_prefecture_ids(user_id=self._user_id)
        return id_list
