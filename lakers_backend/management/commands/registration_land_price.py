import logging
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand, CommandError

from lakers_backend.management.commands.usecase.load_land_price import main

JST = ZoneInfo("Asia/Tokyo")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "公示価格データ（geojson形式）のLoadコマンド"

    def add_arguments(self, parser):
        parser.add_argument("--geojson", type=str, required=True)

    def handle(self, *args, **options):
        try:
            geojson_path = options["geojson"]
            main(geojson_path)
            print("公示価格データの登録が完了しました")
        except Exception as e:
            logger.exception("公示価格データの登録に失敗しました")
            raise CommandError("公示価格データの登録に失敗しました") from e
