import pathlib
from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from django.core.management import call_command
from django.utils import timezone

from data_models.models import RealEstateReceptionBook, ReceptionBookImport

tz = timezone.get_current_timezone()

JST = ZoneInfo("Asia/Tokyo")
RAW_CSV_NAME = "input_load_book_csv.csv"
BAD_RAW_CSV_NAME = "bad_input_load_book_csv.csv"

TEMP_DIR = f"tests/outputs/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
pathlib.Path(TEMP_DIR).mkdir()


@pytest.fixture(scope="function", autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("LAKERS_OUTPUTS_BASE", TEMP_DIR)


@pytest.mark.django_db
def test_load_book_csv(db, mocker):  # pylint: disable=W0613
    mocker.patch(
        "lakers_backend.management.commands.usecase.load_book_csv_usecase.current_time",
        return_value=datetime(2023, 8, 5, 11, 22, 33, tzinfo=JST),
    )
    raw_csv_path = f"tests/management/data/{RAW_CSV_NAME}"
    call_command("load_book_csv", csv=raw_csv_path, pref="神奈川県", year=2023)
    # 出力されたcsvの確認
    expected_output_csv = pathlib.Path(
        f"{TEMP_DIR}/20230805-112233_converted_{RAW_CSV_NAME}"
    )
    assert expected_output_csv.exists()
    # panderaで　pydantic TypeError: metaclass conflictとなるので遅延import
    import pandas as pd

    raw_csv_df = pd.read_csv(raw_csv_path)
    output_csv_df = pd.read_csv(expected_output_csv)
    assert len(output_csv_df) == len(raw_csv_df)
    # 出力されるはずの内容のcsv Kamitaroさんscriptで生成されたcsv
    correct_csv = pathlib.Path("tests/management/data/correct_load_book_csv.csv")
    assert expected_output_csv.read_text(encoding="utf-8") == correct_csv.read_text(
        encoding="utf-8"
    )
    # 台帳Tableの確認
    assert RealEstateReceptionBook.objects.count() == len(raw_csv_df)
    book = RealEstateReceptionBook.objects.get(
        legal_affairs_bureau_reception_number="1",
        prefectures_city_id=720,
        kaoku_number="53-1-1",
    )
    assert book.chiban == ""  # None to Blank されている
    assert book.kaoku_number == "53-1-1"
    assert book.reception_reason == "表題"
    assert book.is_new is True
    assert book.address == "横浜市中区根岸町"
    assert book.outside is None
    assert book.legal_affairs_bureau_request_date == date(2023, 1, 4)
    assert book.legal_affairs_bureau_reception_number == "1"
    assert book.prefectures_city_id == 720
    assert book.real_estate_book_type_id == 3
    assert book.real_estate_type_id == 1
    # 県別受付帳取込状況Tableの確認
    import_status = ReceptionBookImport.objects.get(prefectures_id=14)
    assert import_status.import_date == date(2023, 8, 5)
    assert import_status.legal_affairs_bureau_request_month == date(2023, 1, 1)
    for pref_id in [14]:
        import_status = ReceptionBookImport.objects.get(prefectures_id=pref_id)
        assert import_status.import_date == date(2023, 8, 5)
        assert import_status.legal_affairs_bureau_request_month == date(2023, 1, 1)


@pytest.mark.django_db
def test_load_book_csv_legal_affairs_bureau_request_date_yyyy_mm_dd(
    db, mocker
):  # pylint: disable=W0613
    """
    法務局受付日がyyyy-mm-dd形式
    """
    mocker.patch(
        "lakers_backend.management.commands.usecase.load_book_csv_usecase.current_time",
        return_value=datetime(2023, 8, 5, 11, 22, 33, tzinfo=JST),
    )
    raw_csv_path = "tests/management/data/input_load_book_csv_yyyymmdd.csv"
    call_command("load_book_csv", csv=raw_csv_path, pref="神奈川県", year=None)
    # 出力されたcsvの確認
    expected_output_csv = pathlib.Path(
        f"{TEMP_DIR}/20230805-112233_converted_input_load_book_csv_yyyymmdd.csv"
    )
    assert expected_output_csv.exists()
    # panderaで　pydantic TypeError: metaclass conflictとなるので遅延import
    import pandas as pd

    raw_csv_df = pd.read_csv(raw_csv_path)
    output_csv_df = pd.read_csv(expected_output_csv)
    assert len(output_csv_df) == len(raw_csv_df)
    # 台帳Tableの確認
    assert RealEstateReceptionBook.objects.count() == len(raw_csv_df)
    book = RealEstateReceptionBook.objects.get(
        legal_affairs_bureau_reception_number="1",
    )
    assert book.legal_affairs_bureau_request_date == date(2023, 8, 18)
    book = RealEstateReceptionBook.objects.get(
        legal_affairs_bureau_reception_number="2",
    )
    assert book.legal_affairs_bureau_request_date == date(2023, 11, 1)


@pytest.mark.django_db
def test_load_book_csv_include_invalid_rows(db, mocker):  # pylint: disable=W0613
    mocker.patch(
        "lakers_backend.management.commands.usecase.load_book_csv_usecase.current_time",
        return_value=datetime(2023, 7, 10, 13, 44, 55, tzinfo=JST),
    )
    raw_csv_path = f"tests/management/data/{BAD_RAW_CSV_NAME}"
    call_command("load_book_csv", csv=raw_csv_path, pref="神奈川県", year=2023)
    # 出力されたcsvの確認
    expected_output_csv = pathlib.Path(
        f"{TEMP_DIR}/20230710-134455_converted_{BAD_RAW_CSV_NAME}"
    )
    assert expected_output_csv.exists()
    # panderaで　pydantic TypeError: metaclass conflictとなるので遅延import
    import pandas as pd

    raw_csv_df = pd.read_csv(raw_csv_path)
    output_csv_df = pd.read_csv(expected_output_csv)
    assert len(output_csv_df) == len(raw_csv_df)
    # 台帳Tableの確認
    assert RealEstateReceptionBook.objects.count() == 3  # 3この正しいデータは登録される
    # 県別受付帳取込状況Tableの確認
    for pref_id in [14]:
        import_status = ReceptionBookImport.objects.get(prefectures_id=pref_id)
        assert import_status.import_date == date(2023, 7, 10)
        assert import_status.legal_affairs_bureau_request_month == date(2023, 1, 1)
    # 出力された不正データcsvの確認
    expected_failed_output_csv = pathlib.Path(
        f"{TEMP_DIR}/20230710-134455_failed_{BAD_RAW_CSV_NAME}"
    )
    assert expected_failed_output_csv.exists()
    text = expected_failed_output_csv.read_text(encoding="UTF-8")
    assert len(text.splitlines()) == 3  # include header
    assert "*,,2023-01-04,12時41分作成登記名義人の氏名等について,1910" in text
    assert "横浜市南区永田みなみ台,外3,2023-09-02,33171,721" in text
    # 出力された不正データ原因csvの確認
    expected_failed_causes_output_csv = pathlib.Path(
        f"{TEMP_DIR}/20230710-134455_failed_causes_{BAD_RAW_CSV_NAME}"
    )
    assert expected_failed_causes_output_csv.exists()
    text = expected_failed_causes_output_csv.read_text(encoding="UTF-8")
    assert len(text.splitlines()) == 3  # include header
    assert "3,outside,is_decimal,外3" in text
    assert (
        '2,legal_affairs_bureau_reception_number,"str_length(None, 20)",12時41分作成登記名義人の氏名等について'
        in text
    )
