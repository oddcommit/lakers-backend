import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from data_models.models import AreaUsePurposeConditions
from lakers_backend.option.city.repositories import CityReader

from .util.publish_condition import (
    build_miniature,
    build_publish_conditions,
    build_published_at,
    calc_publish_plug,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--targetcsv", type=str, required=True)

    def handle(self, *args, **options):
        try:
            print(f"load {options['targetcsv']}")
            target_df = pd.read_csv(options["targetcsv"])
            print("data has loaded")
            for _, target_param in target_df.iterrows():
                target_pref_cities = CityReader.get_prefecture_city_from_names(
                    target_param.都道府県名, target_param.自治体名
                )
                publish_plug = calc_publish_plug(target_param.公開可否)
                publish_conditions = build_publish_conditions(
                    publish_plug, target_param.公開条件
                )
                published_at = build_published_at(target_param.参照図作成年)
                miniature = build_miniature(target_param.参照図縮尺)
                for target_pref_city in target_pref_cities:
                    with transaction.atomic():
                        AreaUsePurposeConditions.objects.create(
                            prefecture_city=target_pref_city,
                            conditions=publish_conditions,
                            published_at=published_at,
                            publish_flag=publish_plug,
                            miniature=miniature,
                        )
                    print(f"params: {target_pref_city} has added")
        except RuntimeError:
            print("用途地域公開テーブル追加失敗しました")
