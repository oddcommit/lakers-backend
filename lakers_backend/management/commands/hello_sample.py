import os

from django.core.management.base import BaseCommand

from data_models.models import Prefectures


class Command(BaseCommand):
    help = "sample"

    def handle(self, *args, **options):
        db_host = os.environ.get("DB_HOST", "getting_DB_HOST_failed")

        print(f"Hello World! {db_host=}")
        print("print Prefectures start")
        for data in Prefectures.objects.all():
            print(data.__dict__)
