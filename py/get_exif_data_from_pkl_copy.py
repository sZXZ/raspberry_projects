import pandas as pd
import numpy as np
import exifread
import argparse
import os


def get_context():
    parser = argparse.ArgumentParser(description="pkl path in name format without .pkl")
    parser.add_argument("-p", "--pkl")
    parser.add_argument("-b", "--backup", default=5)
    return parser.parse_args()


def save_data(name, data):
    for key in data.keys():
        
    print("\n\nsaved")

def append_to_file(name, data):
    with open(f"{name}.csv", "a") as f:
        f.write(f"{data}\n")

def do(context):
    name = str(context.pkl)
    backup_rate = int(context.backup)
    df = pd.read_pickle(f"{name}.pkl")
    gather_data = {
        "name": [],
        "Image ImageWidth": [],
        "Image ImageLength": [],
        "Image Model": [],
        # "GPS GPSVersionID": [],
        # "Image GPSInfo": [],
        "EXIF ExposureTime": [],
        "EXIF FNumber": [],
        "EXIF ExposureProgram": [],
        "EXIF ISOSpeedRatings": [],
        # "EXIF ExifVersion": [],
        "EXIF DateTimeOriginal": [],
        # "EXIF DateTimeDigitized": [],    # "EXIF ComponentsConfiguration": [],    # "EXIF ShutterSpeedValue": [],
        # "EXIF ApertureValue": [],    # "EXIF ExposureBiasValue": [],    # "EXIF MeteringMode": [],    # "EXIF Flash": [],
        # "EXIF FocalLength": [],    # "EXIF SubSecTime": [],    # "EXIF SubSecTimeOriginal": [],
        # "EXIF SubSecTimeDigitized": [],    # "EXIF FlashPixVersion": [],    # "EXIF ColorSpace": [],
        # "EXIF ExifImageWidth": [],    # "EXIF ExifImageLength": [],
        # "Interoperability InteroperabilityIndex": [],    # "Interoperability InteroperabilityVersion": [],
        # "EXIF InteroperabilityOffset": [],    # "EXIF FocalPlaneXResolution": [],    # "EXIF FocalPlaneYResolution": [],
        # "EXIF FocalPlaneResolutionUnit": [],    # "EXIF CustomRendered": [],
        "GPS GPSLatitudeRef": [],
        "GPS GPSLatitude": [],
        "GPS GPSLongitudeRef": [],
        "GPS GPSLongitude": [],
        "GPS GPSTimeStamp": [],
        "Image GPSInfo": [],
        "EXIF ExposureMode": [],
        "EXIF WhiteBalance": [],
        "EXIF SceneCaptureType": [],
    }
    # counters
    last_save = 0
    itteration = 0
    length = len(df)
    bad_files = 0
    append_to_file(",".join(gather_data.keys()))
    for index, row in df.iterrows():
        # print progress
        print(
            f"{itteration}/{length}, {itteration/length:.1%}- found {bad_files} bad files",
            end="\r",
        )
        itteration += 1

        #
        file_name = row["name"]
        gather_data["name"].append(file_name)
        try:
            with open(f"/home/ubuntu/yd/{file_name}", "rb") as f:
                tags = exifread.process_file(f, details=False)
                for key in gather_data.keys():
                    if key not in "name":
                        try:
                            gather_data[key].append(tags[key])
                        except:
                            gather_data[key].append(np.nan)
            
        except:
            bad_files += 1
        save_data(name, gather_data)
    # finally save everything
    save_data(name, gather_data)
    print(f"{itteration}/{length}, {itteration/length:.1%} - done")


if __name__ == "__main__":
    do(get_context())
