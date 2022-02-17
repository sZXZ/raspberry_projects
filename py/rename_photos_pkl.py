
import pandas as pd
import numpy as np
from py.utils import yandex_disk
import argparse


def get_context():
    parser = argparse.ArgumentParser(description="pkl path in name format without .pkl")
    parser.add_argument("-p", "--pkl")
    parser.add_argument("-s", "--seperator", default=",")
    parser.add_argument("-c", "--continue_from", default=0, type=int)
    return parser.parse_args()


def append_to_file(name, data_array, seperator):
    with open(f"{name}_renamed.csv", "a") as f:
        f.write(f"{seperator.join(data_array)}\n")


def do(context):
    name = str(context.pkl)
    seperator = context.seperator
    continue_from = int(context.continue_from)
    print(seperator)
    df = pd.read_pickle(f"{name}.pkl")
    if continue_from > 0:
        print(f"starting from {continue_from}")
        df = df[continue_from:]
    
    # counters
    last_save = 0
    itteration = 0
    length = len(df)
    bad_files = 0
    
    y = yandex_disk.YandexDisk()
    
    
    if continue_from == 0:
        append_to_file(name, ['old','new'], seperator)
    for index, row in df.iterrows():
        print(
            f"{itteration}/{length}, {itteration/length:.1%} - "
        )
        old_name = row['name']
        new_name = row['new_name']
        y.rename_file(old_name, new_name)
        append_to_file(name, [old_name, new_name], seperator)
        itteration += 1
    print(f"{itteration}/{length}, {itteration/length:.1%} - done")


if __name__ == "__main__":
    do(get_context())
