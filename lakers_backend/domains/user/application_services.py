from typing import Generic, TypeVar

from .repositories import IUserReader

T = TypeVar("T")


class UserService(Generic[T]):
    def __init__(self, reader: IUserReader, user_id: int):
        self._reader = reader
        self._user_id = user_id

    def is_superuser(self) -> bool:
        is_super_user = self._reader.is_super_user(user_id=self._user_id)
        return is_super_user
