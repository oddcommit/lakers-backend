import logging

from django.core.management.base import BaseCommand, CommandError

from lakers_backend.management.commands.usecase.to_land_and_building_from_book_usecase import (
    main,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "既存の台帳データから土地と建物テーブルのデータを生成"

    def handle(self, *args, **options):
        try:
            print("既存の台帳データから土地と建物テーブルのデータを生成します")
            main()
            print("既存の台帳データから土地と建物テーブルのデータを生成しました")
        except Exception as e:
            logger.exception("既存の台帳データからの土地と建物テーブルのデータ生成に失敗しました")
            raise CommandError("既存の台帳データからの土地と建物テーブルのデータ生成に失敗しました") from e
