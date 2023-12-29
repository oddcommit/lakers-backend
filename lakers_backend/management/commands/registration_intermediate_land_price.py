import logging
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand, CommandError

from lakers_backend.management.commands.usecase.link_land_price_to_land import main

JST = ZoneInfo("Asia/Tokyo")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "土地データと公示価格データの中間テーブル作成コマンド"

    def add_arguments(self, parser):
        parser.add_argument(
            "--add_data_type",
            type=str,
            required=True,
            choices=["land", "land_price"],
            help="土地データ投入後は「land」、公示価格データ投入後は「land_price」を入力してください",
        )

    def handle(self, *args, **options):
        try:
            add_data_type = options["add_data_type"]
            main(add_data_type)
            print("土地データと公示価格データの紐付けが完了しました")
        except Exception as e:
            logger.exception("土地データと公示価格データの紐付けに失敗しました")
            raise CommandError("土地データと公示価格データの紐付けに失敗しました") from e
