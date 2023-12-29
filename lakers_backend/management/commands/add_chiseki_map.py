import os

from django.core.management.base import BaseCommand

from .data_input.load_chiseki_map import load_all_properties


class Command(BaseCommand):
    help = "地積データフレーム生成コマンド"

    def add_arguments(self, parser):
        parser.add_argument("--targetdir", type=str, required=True)
        parser.add_argument("--mode", type=str, default="jsonl")
        parser.add_argument("--dfoutput", type=str, default="dataframe")

    def handle(self, *args, **options):
        try:
            target_df = load_all_properties(
                options["targetdir"], options["mode"] == "jsonl"
            )
            df_pickle_name = os.path.basename(options["targetdir"])
            os.makedirs(options["dfoutput"], exist_ok=True)
            target_dir_path = os.path.join(options["dfoutput"], df_pickle_name)
            target_df.to_pickle(f"{target_dir_path}.pkl")

        except RuntimeError:
            print("地積追加失敗しました")
