from django.test import TestCase
from factory import LandsFactory

from lakers_backend.management.commands.util.run_connect_land_to_area_use_purpose import (
    create_or_update_connect,
)
from tests.application.option.area_use_purpose.factory import AreaUsePurposeFactory


class RunConnectLandToAreaUseTest(TestCase):
    def setUp(self):
        self.registration_map = LandsFactory.build_registration_map()
        self.lands = LandsFactory.build_lands()

        self.area_use_purpose_conditions = (
            AreaUsePurposeFactory.build_area_use_purpose_conditions()
        )
        self.area_use_purpose_types = (
            AreaUsePurposeFactory.build_area_use_purpose_type()
        )
        self.area_use_purpose = AreaUsePurposeFactory.build_area_use_purpose(
            self.area_use_purpose_types[0],
            self.area_use_purpose_conditions[0],
            [[[5, 5], [10, 5], [10, 10], [5, 10]]],
        )

    def test__用途地域と土地テーブルの結びつきが一切されていない場合結びつけられる(self):
        land = self.lands[0]
        result = create_or_update_connect(land, self.area_use_purpose)
        self.assertEqual(result.land, land)
        self.assertEqual(result.area_use_purpose, self.area_use_purpose)

    def test__用途地域と土地テーブルの結びつきがされているものの場合更新される(self):
        land = self.lands[0]
        base_connect = create_or_update_connect(land, self.area_use_purpose)
        land.chiban = "test"
        result = create_or_update_connect(land, self.area_use_purpose)
        self.assertEqual(result.land.chiban, "test")
        self.assertEqual(result.land.id, base_connect.land.id)
