from django.core.management.base import BaseCommand

from .util.run_add_geoinfo import run_add_geoinfo


class Command(BaseCommand):
    help = "地積に緯度経度付与情報追加"

    def add_arguments(self, parser):
        parser.add_argument("--inputdffile", type=str, required=True)
        parser.add_argument("--outputdffile", type=str, required=True)

    def handle(self, *args, **options):
        run_add_geoinfo(options["inputdffile"], options["outputdffile"])
