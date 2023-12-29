from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from data_models.models import Plan, User

from .util.calc_term import calc_term
from .util.connect_plan_to_user import connect_plan_to_user


class Command(BaseCommand):
    help = "一般ユーザープラン結びつけコマンド"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True)
        parser.add_argument("--plantypename", type=str, required=True)
        parser.add_argument("--planstartdate", type=str, required=True)

    def handle(self, *args, **options):
        try:
            plan_start_date, plan_end_date = calc_term(options["planstartdate"])
            plan_type_name = options["plantypename"]
            plans = Plan.objects.filter(plan_type__name=plan_type_name).all()
            if len(plans) == 0:
                raise CommandError("プラン紐付けを失敗しました 対象となるプランが存在しません")
            user = User.objects.get(email=options["email"])

            with transaction.atomic():
                connect_plan_to_user(user, plans, plan_start_date, plan_end_date)
                print(f"ユーザー{user.email}にプラン{plan_type_name}を紐づけました")
        except User.DoesNotExist as e:
            raise CommandError("プラン紐付けを失敗しました 対象となるユーザーが存在しません") from e
        except RuntimeError:
            print("プラン紐付けを失敗しました")
