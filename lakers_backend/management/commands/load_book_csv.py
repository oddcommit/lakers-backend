import logging
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand, CommandError

from lakers_backend.management.commands.usecase.load_book_csv_usecase import main

JST = ZoneInfo("Asia/Tokyo")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "台帳CSVのLoadコマンド"

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str, required=True)
        parser.add_argument("--pref", type=str, required=True)
        parser.add_argument("--year", type=int)

    def handle(self, *args, **options):
        try:
            csv_path = options["csv"]
            prefecture = options["pref"]
            year = options["year"]
            main(csv_path, prefecture, year)
            print("台帳CSVをLoadしました")
        except Exception as e:
            logger.exception("台帳CSVのLoadに失敗しました")
            raise CommandError("台帳CSVのLoadに失敗しました") from e
