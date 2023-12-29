import json

import pandas as pd
import swifter  # NOQA pylint: disable=W0611 並列化のためにインポートする必要あるため 仕様上構文解析に乗らず使われていない扱いになってしまう
from pandas import json_normalize


def load_geojson(file_path: str) -> pd.DataFrame:
    with open(file_path, encoding="utf-8") as f:
        print(f"load {file_path}")
        raw_dataset = json.load(f)
        base_df = pd.DataFrame(raw_dataset["features"])
        df = json_normalize(base_df["properties"].apply(lambda x: x))
        df_coordinates = json_normalize(base_df["geometry"].apply(lambda x: x))
        df["coordinates"] = df_coordinates.coordinates
        print(f"file {file_path} has loaded")
        return df
