import pytest

from lakers_backend.management.commands.usecase.load_book_csv_usecase import (
    is_new,
    real_estate_reception_book_type,
    real_estate_type,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("連先", 1),
        ("連続", 2),
        ("単独", 3),
        ("invalid_str", None),
    ],
    ids=["連先", "連続", "単独", "invalid_str"],
)
def test_real_estate_reception_book_type(test_input, expected):
    assert real_estate_reception_book_type(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("建物", 1),
        ("土地", 2),
        ("区建", 3),
        ("共担", 4),
        ("その他", 5),
        ("一棟", 6),
        ("invalid_str", None),
    ],
    ids=["建物", "土地", "区建", "共担", "その他", "一棟", "invalid_str"],
)
def test_real_estate_type(test_input, expected):
    assert real_estate_type(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("新", True),
        ("既", False),
        ("", False),
    ],
    ids=["新", "既", "から文字"],
)
def test_is_new(test_input, expected):
    assert is_new(test_input) is expected
