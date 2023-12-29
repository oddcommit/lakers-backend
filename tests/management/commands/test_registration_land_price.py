import pandas as pd
import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from data_models.models import PublicLandPrice
from lakers_backend.management.commands.usecase.load_land_price import (
    split_syozai_for_land_price,
)


class TestLancPrice:
    @pytest.mark.django_db
    def test_registration_land_price(self, caplog):  # pylint: disable=W0613
        """DBへ登録する場合"""
        geojson_path = "tests/management/data/L01-23_13.geojson"
        call_command("registration_land_price", geojson=geojson_path)

        # 公示価格Tableの確認
        assert PublicLandPrice.objects.count() == 2602
        price = PublicLandPrice.objects.all()
        assert price[0].location == "千代田区三番町"
        assert price[0].chiban == "6-25"
        assert price[0].land_price == 3340000
        assert price[0].jukyo_hyoji == ""
        assert price[0].latitude == 35.69014
        assert price[0].longitude == 139.744815
        assert price[0].prefectures_id == 13

        # 同じデータを2回登録した場合
        try:
            call_command("registration_land_price", geojson=geojson_path)
        except CommandError:
            assert "公示価格データの登録に失敗しました" in caplog.text
        assert PublicLandPrice.objects.count() == 2602

    @pytest.mark.django_db
    def test_cannot_read_file_type(self, caplog):  # pylint: disable=W0613
        """geojson以外のファイルを読み込んだ場合"""
        geojson_path = "tests/management/data/L01-23_13.csv"
        try:
            call_command("registration_land_price", geojson=geojson_path)
        except CommandError:
            assert "公示価格データの登録に失敗しました" in caplog.text

    @pytest.mark.django_db
    def test_registration_land_price_split_unit(self):  # pylint: disable=W0613
        """分割ロジックの検証"""

        df_target = split_syozai_for_land_price(
            pd.DataFrame(
                [
                    # L167のパターン
                    [
                        25962,
                        "沖縄県 中頭郡北谷町美浜2丁目1番3外",
                        235000,
                        2023,
                        "",
                        127.76045111100007,
                        26.314943889000062,
                    ],
                    # L171のパターン
                    [
                        1719,
                        "岩手県 花巻市石鳥谷町好地第16地割106番1内",
                        23000,
                        2023,
                        "",
                        141.15226305600004,
                        39.49371305600005,
                    ],
                    # L177のパターン
                    [
                        629,
                        "北海道 旭川市東鷹栖2線15号671番8内",
                        3000,
                        2023,
                        "",
                        142.42763388900005,
                        43.83362305600008,
                    ],
                    # L181のパターン
                    [
                        1322,
                        "北海道 河西郡芽室町北芽室北4線6番2",
                        1800,
                        2023,
                        "",
                        143.075003056,
                        42.942476111000076,
                    ],
                    # L186のパターン
                    [
                        23793,
                        "福岡県 福岡市中央区草香江2丁目12区220番1",
                        603000,
                        2023,
                        "草香江2−12−16",
                        130.37225888900002,
                        33.58160611100004,
                    ],
                    # L190のパターン
                    [
                        18137,
                        "大阪府 堺市西区浜寺船尾町東4丁1番外",
                        174000,
                        2023,
                        "",
                        135.45913611100002,
                        34.54709694400003,
                    ],
                    # L195のパターン
                    [
                        22750,
                        "徳島県 徳島市佐古八番町佐16の21番7",
                        89700,
                        2023,
                        "佐古八番町2−3",
                        134.52209805600012,
                        34.076418889000024,
                    ],
                    # L198のパターン
                    [
                        24119,
                        "福岡県 大川市大字榎津字油田239・240番合併10",
                        28400,
                        2023,
                        "",
                        130.37720611100008,
                        33.20653694400005,
                    ],
                    # L200のパターン
                    [
                        24872,
                        "熊本県 熊本市西区春日3丁目2146",
                        198000,
                        2023,
                        "春日3−19−8",
                        130.687436111,
                        32.79171027800004,
                    ],
                    # L202のパターン
                    [
                        1033,
                        "北海道 深川市2条2921番22",
                        5900,
                        2023,
                        "2条21−21",
                        142.06028305600012,
                        43.72579305600004,
                    ],
                ],
                columns=[
                    "",
                    "L01_024",
                    "L01_006",
                    "L01_005",
                    "L01_025",
                    "longitude",
                    "latitude",
                ],
            )
        )

        result_image = pd.DataFrame(
            [
                # L167のパターン
                [
                    25962,
                    235000,
                    2023,
                    "",
                    127.76045111100007,
                    26.314943889000062,
                    "沖縄県",
                    "中頭郡北谷町美浜2丁目",
                    "1-3",
                ],
                # L171のパターン
                [
                    1719,
                    23000,
                    2023,
                    "",
                    141.15226305600004,
                    39.49371305600005,
                    "岩手県",
                    "花巻市石鳥谷町好地第16地割",
                    "106-1",
                ],
                # L177のパターン
                [
                    629,
                    3000,
                    2023,
                    "",
                    142.42763388900005,
                    43.83362305600008,
                    "北海道",
                    "旭川市東鷹栖2線15号",
                    "671-8",
                ],
                # L181のパターン
                [
                    1322,
                    1800,
                    2023,
                    "",
                    143.075003056,
                    42.942476111000076,
                    "北海道",
                    "河西郡芽室町北芽室北4線",
                    "6-2",
                ],
                # L186のパターン
                [
                    23793,
                    603000,
                    2023,
                    "草香江2−12−16",
                    130.37225888900002,
                    33.58160611100004,
                    "福岡県",
                    "福岡市中央区草香江2丁目12区",
                    "220-1",
                ],
                # L190のパターン
                [
                    18137,
                    174000,
                    2023,
                    "",
                    135.45913611100002,
                    34.54709694400003,
                    "大阪府",
                    "堺市西区浜寺船尾町東4丁",
                    "1",
                ],
                # L195のパターン
                [
                    22750,
                    89700,
                    2023,
                    "佐古八番町2−3",
                    134.52209805600012,
                    34.076418889000024,
                    "徳島県",
                    "徳島市佐古八番町",
                    "佐16の21-7",
                ],
                # L198のパターン
                [
                    24119,
                    28400,
                    2023,
                    "",
                    130.37720611100008,
                    33.20653694400005,
                    "福岡県",
                    "大川市大字榎津字油田",
                    "239・240-合併10",
                ],
                # L200のパターン
                [
                    24872,
                    198000,
                    2023,
                    "春日3−19−8",
                    130.687436111,
                    32.79171027800004,
                    "熊本県",
                    "熊本市西区春日3丁目",
                    "2146",
                ],
                # L202のパターン
                [
                    1033,
                    5900,
                    2023,
                    "2条21−21",
                    142.06028305600012,
                    43.72579305600004,
                    "北海道",
                    "深川市2条",
                    "2921-22",
                ],
            ],
            columns=[
                "",
                "L01_006",
                "L01_005",
                "L01_025",
                "longitude",
                "latitude",
                "todofuken",
                "location",
                "chiban",
            ],
        )

        assert result_image.equals(df_target)
