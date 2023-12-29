import pandas as pd
from pandarallel import pandarallel

from ..util.add_land import add_registration_map_and_land

pandarallel.initialize(progress_bar=True)


def run_add_land(target_df_file: str):
    try:
        target_df = pd.read_pickle(target_df_file)
        target_df.parallel_apply(add_registration_map_and_land, axis=1)
    except RuntimeError:
        print("地積追加失敗しました")
