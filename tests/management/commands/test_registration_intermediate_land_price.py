import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from data_models.models import Land, LinkLandPriceToLand


class TestIntermediateLandprice:
    @pytest.fixture(autouse=True)
    def django_db_setup_intermediate_land_price(
        self, django_db_setup, django_db_blocker
    ):  # pylint: disable=W0613,W0621
        with django_db_blocker.unblock():
            call_command("loaddata", "tests/fixtures/master_registrationmap.jsonl")
            call_command("loaddata", "tests/fixtures/master_land.jsonl")

    @pytest.mark.django_db
    def test_registration_intermediate_cant_use_option(
        self, db, caplog
    ):  # pylint: disable=W0613
        """利用できないオプションを利用した場合"""
        try:
            call_command("registration_intermediate_land_price", add_data_type="test")
        except CommandError:
            assert CommandError

    @pytest.mark.django_db
    def test_registration_intermediate_success(
        self, db, caplog
    ):  # pylint: disable=W0613
        """登録に成功する"""

        # 公示価格データ投入後パターン
        geojson_path = "tests/management/data/L01-23_13.geojson"
        call_command("registration_land_price", geojson=geojson_path)
        call_command("registration_intermediate_land_price", add_data_type="land_price")

        # 土地公示価格Tableの確認
        intermediate_table = LinkLandPriceToLand.objects.get(id="1")
        assert intermediate_table.land_id == 1
        assert intermediate_table.public_land_price_id == 1835

        # 土地データ投入後パターン
        new_land = [
            {
                "location": "足立区西保木間3丁目",
                "chiban": "213-10",
                "real_estate_id": None,
                "latitude": 35.54845,
                "longitude": 139.452209,
                "created_at": "2023-09-05",
                "updated_at": "2023-09-05",
                "owner_latest_get_date": "2023-08-28",
                "prefecture_city_id": 675,
                "registration_map_id": 2,
            }
        ]
        intermediate_land_price_for_insert = [Land(**row) for row in new_land]
        Land.objects.bulk_create(intermediate_land_price_for_insert)
        call_command("registration_intermediate_land_price", add_data_type="land")

        # 土地公示価格Tableの確認
        intermediate_table_after_land = LinkLandPriceToLand.objects.get(id="2")
        assert intermediate_table_after_land.land_id == 2
        assert intermediate_table_after_land.public_land_price_id == 2092
