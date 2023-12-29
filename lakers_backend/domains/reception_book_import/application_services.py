from typing import Generic, TypeVar

from .objects import ReceptionBookImportEntity
from .repositories import IReceptionBookImportReader

T = TypeVar("T")


class ReceptionBookImportService(Generic[T]):
    def __init__(self, reader: IReceptionBookImportReader, data: T):
        self._reader = reader
        self._data = data

    def execute(self) -> list[ReceptionBookImportEntity]:
        domain_list = self._reader.read()
        return domain_list
