from logging import INFO

import pytest
from django.core.management import call_command

from data_models.models import (
    Building,
    BuildingAreaUsePurpose,
    Land,
    LandAreaUsePurpose,
    RealEstateReceptionBook,
)


@pytest.fixture(autouse=True)
def setup_books(django_db_setup, django_db_blocker):  # pylint: disable=W0613,W0621
    with django_db_blocker.unblock():
        call_command(
            "loaddata", "tests/fixtures/to_land_and_building_from_book/13-book.jsonl"
        )
        call_command(
            "loaddata", "tests/fixtures/to_land_and_building_from_book/14-book.jsonl"
        )


@pytest.fixture(scope="module", autouse=True)
def setup_area_use_purpose(
    django_db_setup, django_db_blocker
):  # pylint: disable=W0613,W0621
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            "tests/fixtures/to_land_and_building_from_book/area_use_purpose_type.jsonl",
        )
        call_command(
            "loaddata",
            "tests/fixtures/to_land_and_building_from_book/area_use_purpose_conditions.jsonl",
        )
        call_command(
            "loaddata",
            "tests/fixtures/to_land_and_building_from_book/area_use_purpose.jsonl",
        )


@pytest.mark.django_db
def test_to_land_and_building_from_book(db):  # pylint: disable=W0613
    call_command("to_land_and_building_from_book")
    # 東京都
    # 1(建物) -> 建物TBL: 2個(３件あるが１件は所在が重複のため除かれているはず。prefectures_city: 663, kaoku_number": 423-71)
    # 2(土地) -> 土地TBL: 2個(３件あるが１件は所在が重複のため除かれているはず。prefectures_city: 665, chiban": 612-1)
    # 3(区分建物) -> 建物TBL: 3個
    # 4(共担) -> SKIP: 1個
    # 5(その他) -> SKIP: 1個
    # 6(一棟) -> 建物TBL: 1個
    # null -> SKIP: 2個
    building_type_count_map = {
        1: 2,
        3: 3,
        6: 1,
    }
    for building_type, expected_count in building_type_count_map.items():
        count = Building.objects.filter(
            prefecture_city__prefectures=13,
            real_estate_type_id=building_type,
        ).count()
        assert count == expected_count
    # 建物
    building = Building.objects.get(
        prefecture_city__id=663,
        kaoku_number="423-71",
    )
    assert building is not None
    assert building.real_estate_type.id == 1
    assert (building.longitude, building.latitude) == (139.710815, 35.622345)
    # 用途地域中間TBL
    building_area_use_purpose = BuildingAreaUsePurpose.objects.get(building=building)
    assert building_area_use_purpose is not None
    assert building_area_use_purpose.area_use_purpose.prefecture_city_id == 663
    # 台帳データ
    for book in RealEstateReceptionBook.objects.filter(
        prefectures_city=663,
        kaoku_number="423-71",
    ):
        # 既存の建物がある台帳データも無い台帳データも両方、建物と紐づいている
        assert book.building == building

    # 土地
    count = Land.objects.filter(
        prefecture_city__prefectures=13,
    ).count()
    assert count == 2
    land = Land.objects.get(
        prefecture_city__id=665,
        chiban="612-1",
    )
    assert land is not None
    assert land.location == "大田区池上3丁目"
    assert (land.longitude, land.latitude) == (139.701126, 35.575581)
    # 用途地域中間TBL
    land_area_use_purpose = LandAreaUsePurpose.objects.get(land=land)
    assert land_area_use_purpose is not None
    assert land_area_use_purpose.area_use_purpose.prefecture_city_id == 665
    # 台帳データ
    for book in RealEstateReceptionBook.objects.filter(
        prefectures_city=665,
        chiban="612-1",
    ):
        # 既存の土地がある台帳データも無い台帳データも両方、土地と紐づいている
        assert book.land == land

    # 神奈川県
    # 1(建物) -> 建物TBL: 1個(2件あるが１件は所在が重複のため除かれているはず。prefectures_city: 720, kaoku_number": 131-11)
    # 2(土地) -> 土地TBL: 2個
    # 3(区分建物) -> 建物TBL: 2個
    # 4(共担) -> SKIP: 2個
    # 5(その他) -> SKIP: 0個
    # 6(一棟) -> 建物TBL: 0個
    # null -> SKIP: 2個
    building_type_count_map = {
        1: 1,
        3: 2,
        6: 0,
    }
    for building_type, expected_count in building_type_count_map.items():
        count = Building.objects.filter(
            prefecture_city__prefectures=14,
            real_estate_type_id=building_type,
        ).count()
        assert count == expected_count
    # 土地
    count = Land.objects.filter(
        prefecture_city__prefectures=14,
    ).count()
    assert count == 2


@pytest.mark.django_db
def test_to_land_and_building_from_book_only_tokyo_kanagawa(
    db, monkeypatch
):  # pylint: disable=W0613
    monkeypatch.setenv("LAKERS_TARGET_PREFECTURES", "13,14")
    call_command("to_land_and_building_from_book")
    assert Building.objects.filter(prefecture_city__prefectures=13).count() > 0
    assert Land.objects.filter(prefecture_city__prefectures=13).count() > 0
    assert Building.objects.filter(prefecture_city__prefectures=14).count() > 0
    assert Land.objects.filter(prefecture_city__prefectures=14).count() > 0


@pytest.mark.django_db
def test_to_land_and_building_from_book_only_tokyo(
    db, monkeypatch
):  # pylint: disable=W0613
    monkeypatch.setenv("LAKERS_TARGET_PREFECTURES", "13")
    call_command("to_land_and_building_from_book")
    assert Building.objects.filter(prefecture_city__prefectures=13).count() > 0
    assert Land.objects.filter(prefecture_city__prefectures=13).count() > 0
    # 神奈川県は未処理のためゼロ
    assert Building.objects.filter(prefecture_city__prefectures=14).count() == 0
    assert Land.objects.filter(prefecture_city__prefectures=14).count() == 0


@pytest.mark.django_db
def test_to_land_and_building_from_book_only_tokyo_chunk_cities_dry_run(
    db, monkeypatch, caplog
):  # pylint: disable=W0613
    monkeypatch.setenv("LAKERS_TARGET_PREFECTURES", "13")
    monkeypatch.setenv("LAKERS_TARGET_CITIES_CHUNK", "1/10")
    monkeypatch.setenv("LAKERS_BATCH_DRY_RUN", "1")  # 処理は行わない
    call_command("to_land_and_building_from_book")
    assert Building.objects.filter(prefecture_city__prefectures=13).count() == 0
    assert Land.objects.filter(prefecture_city__prefectures=13).count() == 0
    assert Building.objects.filter(prefecture_city__prefectures=14).count() == 0
    assert Land.objects.filter(prefecture_city__prefectures=14).count() == 0
    mod_name = "lakers_backend.management.commands.usecase.to_land_and_building_from_book_usecase"
    # ここから
    assert (mod_name, INFO, "東京都千代田区の処理を開始します") in caplog.record_tuples
    assert (mod_name, INFO, "東京都墨田区の処理を開始します") in caplog.record_tuples
    # ↑ここまで
    assert (mod_name, INFO, "東京都江東区の処理を開始します") not in caplog.record_tuples
    # 東京都は63cities
    num_cities = 0
    for log_rec in caplog.record_tuples:
        if log_rec[0] == mod_name and "区の処理を開始します" in log_rec[2]:
            num_cities += 1
    assert num_cities == 7
