import csv
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand

from data_models.models import PrefecturesCity, ReceptionBookImport

JST = ZoneInfo("Asia/Tokyo")


class Command(BaseCommand):
    """
    TODO 削除予定。load_book_csv.pyで一括対応することになった。
    """

    help = "県別受付帳取込状況反映コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str, required=True)

    def handle(self, *args, **options):
        # pylint: disable=W1514 このファイルはもうすぐ不要となる
        try:
            now = datetime.now(JST)
            csv_path = options["csv"]
            with open(csv_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                row = next(reader)  # 1行目のみ
                request_date = row["legal_affairs_bureau_request_date"]
                request_date_day1 = datetime.strptime(request_date, "%Y-%m-%d").replace(
                    tzinfo=JST, day=1
                )
                prefectures_city_id = row["prefectures_city_id"]
                pref_city = PrefecturesCity.objects.get(city_id=prefectures_city_id)
                ReceptionBookImport.objects.create(
                    prefectures_id=pref_city.prefectures_id,
                    import_date=now.date(),
                    legal_affairs_bureau_request_month=request_date_day1,
                )
            print("県別受付帳取込状況を反映しました")
        except RuntimeError:
            print("県別受付帳取込状況の反映に失敗しました")
