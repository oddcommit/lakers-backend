from django.core.management.base import BaseCommand
from django.db import transaction

from data_models.models import PlanType


class Command(BaseCommand):
    help = "プラン種別作成コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--plantypename", type=str, required=True)
        parser.add_argument("--price", type=int, required=True)

    def handle(self, *args, **options):
        try:
            plan_type_name = options["plantypename"]
            price = options["price"]
            with transaction.atomic():
                PlanType.objects.create(
                    name=plan_type_name,
                    price=price,
                ).save()
            print(f"プラン種別{plan_type_name}を作成しました")
        except RuntimeError:
            print("プラン種別の作成に失敗しました")
