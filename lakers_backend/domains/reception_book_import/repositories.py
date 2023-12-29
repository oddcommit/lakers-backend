from abc import abstractmethod
from typing import List

from .objects import ReceptionBookImportEntity


class IReceptionBookImportReader:
    @abstractmethod
    def read(self) -> List[ReceptionBookImportEntity]:
        raise NotImplementedError()
