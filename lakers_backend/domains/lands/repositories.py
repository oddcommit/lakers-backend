from abc import ABC, abstractmethod

from data_models.models import Land


class ILands(ABC):
    @staticmethod
    @abstractmethod
    def get_lands(will_ignore_connected_area_use_purpose: bool) -> list[Land]:
        raise NotImplementedError()
