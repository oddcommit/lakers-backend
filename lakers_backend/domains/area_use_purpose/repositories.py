from abc import ABC, abstractmethod

from data_models.models import AreaUsePurposeConditions, AreaUsePurposeType


class IAreaUsePurpose(ABC):
    @staticmethod
    @abstractmethod
    def get_area_use_purpose_conditions(
        pref_name: str, city_code: str
    ) -> AreaUsePurposeConditions:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_or_create_use_purpose_type(
        purpose_code: str, purpose_name: str
    ) -> AreaUsePurposeType:
        raise NotImplementedError()
