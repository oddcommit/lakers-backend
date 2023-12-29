import glob
from typing import Callable

import pandas as pd


def load_file_paths(dir_path: str, is_jsonl: bool):
    if is_jsonl:
        return sorted(glob.glob(f"{dir_path}/*.jsonl"))
    return sorted(glob.glob(f"{dir_path}/*.geojson"))


def load_all_properties_from_file_paths_common(
    file_paths: list[str], load_data: Callable[[str], pd.DataFrame]
) -> pd.DataFrame:
    base_df = load_data(file_paths[0])
    for file_path in file_paths[1:]:
        other_df = load_data(file_path)
        base_df = pd.concat([base_df, other_df])
    return base_df
