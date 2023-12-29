import os

from django.core.management.base import BaseCommand
from django.db import transaction

from data_models.models import AreaUsePurpose, AreaUsePurposeConditions
from lakers_backend.option.area_use_purpose.repositories import AreaUsePurposeReader

from .data_input.load_area_use_purpose import get_city_code, load_area_use_purposes
from .util.logger import LogFileWriter


class Command(BaseCommand):
    help = "用途地域追加"

    def add_arguments(self, parser):
        parser.add_argument("--targetdir", type=str, required=True)

    def handle(self, *args, **options):
        target_dir_name = os.path.basename(options["targetdir"])
        print(f"file_name add_area_use_purpose_{target_dir_name}.log")
        log_writer = LogFileWriter("log", f"add_area_use_purpose_{target_dir_name}.log")

        try:
            target_df = load_area_use_purposes(options["targetdir"])
            for _, target_param in target_df.iterrows():
                with transaction.atomic():
                    try:
                        target_city_code = get_city_code(target_param.coordinates)
                        area_use_purpose_condition = (
                            AreaUsePurposeReader.get_area_use_purpose_conditions(
                                target_param.都道府県名, target_city_code
                            )
                        )
                        if target_city_code == "999999":
                            log_writer.write_log(
                                f"{target_param['都道府県名']} {target_param['市区町村名']}"
                                f" {target_param.coordinates} cannot found"
                            )
                            continue
                    except AreaUsePurposeConditions.DoesNotExist:
                        log_writer.write_log(
                            f"{target_param['都道府県名']} {target_param['市区町村名']} {target_param.coordinates}"
                            f" {AreaUsePurposeConditions.DoesNotExist}"
                        )
                        continue
                    except TypeError:
                        log_writer.write_log(
                            f"{target_param['都道府県名']} {target_param['市区町村名']} {target_param.coordinates} {TypeError}"
                        )

                        continue
                    area_use_purpose_type = (
                        AreaUsePurposeReader.get_or_create_use_purpose_type(
                            target_param.用途地域コード, target_param.用途地域名
                        )
                    )

                    AreaUsePurpose.objects.create(
                        prefecture_city=area_use_purpose_condition.prefecture_city,
                        geometry={"geometry": target_param.coordinates},
                        area_use_purpose_type=area_use_purpose_type,
                        area_use_purpose_condition=area_use_purpose_condition,
                        building_late=target_param.建蔽率,
                        volume_late=target_param.容積率,
                    )

        except RuntimeError:
            print("用途地域追加失敗しました")
