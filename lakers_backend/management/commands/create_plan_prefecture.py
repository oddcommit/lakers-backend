from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from data_models.models import (
    City,
    Plan,
    PlanArea,
    PlanType,
    Prefectures,
    PrefecturesCity,
)


class Command(BaseCommand):
    help = "プランエリア結びつけ作成コマンド（県単位のプラン）"

    def add_arguments(self, parser):
        parser.add_argument("--prefname", type=str, required=True)
        parser.add_argument("--plantypename", type=str, required=True)

    def handle(self, *args, **options):
        try:
            plan_type_name = options["plantypename"]
            plan_type = PlanType.objects.filter(name=plan_type_name).get()
            if plan_type is None:
                raise CommandError("対象となるプランが存在しません")
            prefecture_name = options["prefname"]
            prefecture = Prefectures.objects.filter(name=prefecture_name).get()
            if prefecture is None:
                raise CommandError(
                    f"都道府県{prefecture_name}をプラン{plan_type_name}との結びつけに失敗しました"
                )
            prefecture_cities = PrefecturesCity.objects.filter(
                prefectures__pref_code=prefecture.id
            ).exclude(city=City.objects.filter(name="不明").get())
            with transaction.atomic():
                for city in prefecture_cities:
                    plan_area = PlanArea.objects.create(
                        plan_name=plan_type_name,
                        prefecture_code=prefecture,
                        city_code=city.city,
                    )
                    plan_area.save()
                    Plan.objects.create(
                        plan_type=plan_type,
                        plan_area=plan_area,
                    ).save()
            print(f"{prefecture_name}をプラン{plan_type_name}に紐づけました")
        except RuntimeError:
            print(f"都道府県{prefecture_name}をプラン{plan_type_name}との結びつけに失敗しました")
