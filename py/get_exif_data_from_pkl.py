import pandas as pd
import numpy as np
import exifread
import argparse
import os


def get_context():
    parser = argparse.ArgumentParser(description="pkl path in name format without .pkl")
    parser.add_argument("-p", "--pkl")
    parser.add_argument("-s", "--seperator", default=",")
    parser.add_argument("-c", "--continue_from", default=0, type=int)
    return parser.parse_args()


def append_to_file(name, data_array, seperator):
    with open(f"{name}_exif.csv", "a") as f:
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
    data_to_get = [
        "name",
        "Image ImageWidth",
        "Image ImageLength",
        "Image Model",
        "EXIF ExposureTime",
        "EXIF FNumber",
        "EXIF ExposureProgram",
        "EXIF ISOSpeedRatings",
        "EXIF DateTimeOriginal",
        "GPS GPSLatitudeRef",
        "GPS GPSLatitude",
        "GPS GPSLongitudeRef",
        "GPS GPSLongitude",
        "GPS GPSTimeStamp",
        "Image GPSInfo",
        "EXIF ExposureMode",
        "EXIF WhiteBalance",
        "EXIF SceneCaptureType",
    ]
    # counters
    last_save = 0
    itteration = 0
    length = len(df)
    bad_files = 0
    if continue_from == 0:
        append_to_file(name, data_to_get, seperator)
    for index, row in df.iterrows():
        # print progress
        print(
            f"{itteration}/{length}, {itteration/length:.1%}- found {bad_files} bad files"
        )

        file_name = row["name"]
        # gather_data["name"].append(file_name)
        data_array = [file_name]
        try:
            with open(f"/home/ubuntu/yd/{file_name}", "rb") as f:
                tags = exifread.process_file(f, details=False)
                for key in data_to_get:
                    if key not in "name":
                        try:
                            data_array.append(str(tags[key]))
                        except Exception as ex:
                            print(ex)
                            data_array.append("")
        except Exception as ex:
            print(ex)
            bad_files += 1
        append_to_file(name, data_array, seperator)
        itteration += 1
    print(f"{itteration}/{length}, {itteration/length:.1%} - done")


if __name__ == "__main__":
    do(get_context())
