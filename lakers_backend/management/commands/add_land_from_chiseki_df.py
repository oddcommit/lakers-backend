from django.core.management.base import BaseCommand
from pandarallel import pandarallel

from .util.run_add_geoinfo import run_add_geoinfo
from .util.run_add_land import run_add_land

pandarallel.initialize(progress_bar=True)


class Command(BaseCommand):
    help = "地積データフレームを元に土地テーブルおよび法務省登記所備付地図データテーブル追加コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--inputdffile", type=str, required=True)
        parser.add_argument("--outputdffile", type=str, required=True)

    def handle(self, *args, **options):
        print(
            f"start add geoinfo from {options['inputdffile']} to {options['outputdffile']}"
        )
        run_add_geoinfo(options["inputdffile"], options["outputdffile"])
        print("add geoinfo has finished")
        print(f"start record land table from {options['outputdffile']}")
        run_add_land(options["outputdffile"])
        print("record land table has finished")
