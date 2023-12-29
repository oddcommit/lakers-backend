from django.core.management.base import BaseCommand

from lakers_backend.option.lands.repositories import LandsReader

from .util.run_connect_land_to_area_use_purpose import run_connect


class Command(BaseCommand):
    help = "土地テーブルと用途地域の結びつけ"

    def add_arguments(self, parser):
        parser.add_argument(
            "--ignoreconnected",
            type=bool,
            default=True,
            description="すでに結びついているものに対して対象外にするかどうか",
        )

    def handle(self, *args, **options):
        will_ignore_connected = options["ignoreconnected"]
        target_lands = LandsReader().get_lands(will_ignore_connected)
        run_connect(target_lands, will_ignore_connected)
