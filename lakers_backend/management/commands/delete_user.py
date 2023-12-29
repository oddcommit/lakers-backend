from django.core.management.base import BaseCommand
from django.db import transaction

from data_models.models import User


class Command(BaseCommand):
    help = "一般ユーザー削除コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                user = User.objects.get(email=options["email"])
                user.delete()
                print("ユーザーを削除しました")
        except User.DoesNotExist:
            print("対象となるユーザーは存在しません")
        except RuntimeError:
            print("ユーザーの削除に失敗しました")
