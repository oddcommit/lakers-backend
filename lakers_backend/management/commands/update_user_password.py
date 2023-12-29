from django.core.management.base import BaseCommand
from django.db import transaction

from data_models.models import User


class Command(BaseCommand):
    help = "ユーザーのパスワード更新コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True)
        parser.add_argument("--password", type=str, required=True)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                user = User.objects.get(email=options["email"])
                user.set_password(options["password"])
                user.save()
                print("パスワードを更新しました")
        except RuntimeError:
            print("パスワードの変更に失敗しました")
