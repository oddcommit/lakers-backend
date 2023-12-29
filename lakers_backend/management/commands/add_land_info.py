from django.core.management.base import BaseCommand
from pandarallel import pandarallel

from .util.run_add_land import run_add_land

pandarallel.initialize(progress_bar=True)


class Command(BaseCommand):
    help = "土地テーブルおよび法務省登記所備付地図データテーブル追加コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--targetdffile", type=str, required=True)

    def handle(self, *args, **options):
        run_add_land(options["targetdffile"])
