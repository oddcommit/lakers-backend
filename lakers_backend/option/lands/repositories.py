from data_models.models import Land, LandAreaUsePurpose
from lakers_backend.domains.lands.repositories import ILands


class LandsReader(ILands):
    @staticmethod
    def get_lands(will_ignore_connected_area_use_purpose: bool) -> list[Land]:
        if will_ignore_connected_area_use_purpose:
            ignore_ids = [
                params[0]
                for params in LandAreaUsePurpose.objects.values_list("land__id").all()
            ]
            if len(ignore_ids) == 0:
                return Land.objects.all()
            return Land.objects.filter(id=[params[0] for params in ignore_ids]).all()
        return Land.objects.all()

    @staticmethod
    def get_connection_of_land_to_area_use_purpose(
        land_id: int, area_use_purpose_id: str
    ) -> LandAreaUsePurpose | None:
        if LandAreaUsePurpose.objects.filter(
            land__id=land_id, area_use_purpose_id=area_use_purpose_id
        ).exists():
            return LandAreaUsePurpose.objects.filter(
                land__id=land_id, area_use_purpose_id=area_use_purpose_id
            ).get()
        return None
