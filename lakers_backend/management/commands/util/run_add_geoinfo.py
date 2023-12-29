import pandas as pd

from ..data_input.load_chiseki_map import build_location_dataset


def run_add_geoinfo(input_df_file: str, output_df_file: str):
    base_df = pd.read_pickle(input_df_file)
    converted_df = build_location_dataset(base_df)
    converted_df.to_pickle(output_df_file)
    print("add geoinfo has completed")
