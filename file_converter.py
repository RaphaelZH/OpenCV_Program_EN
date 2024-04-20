from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import nbformat
import pandas as pd
from pathlib import Path
import pytz

from pprint import pprint


def notebook_selector(path_object):
    return [
        file_object.name
        for file_object in path_object.iterdir()
        if (
            file_object.name.split(".")[-1] == "ipynb"
            and file_object.name.find("(Compressed)") == -1
        )
    ]


def info_collector(course, subpath, file_name, info_dict):
    global dir_notebook
    info_dict["File path"].append(course)
    info_dict["File name"].append(file_name)
    path_object = Path(course.join(dir_notebook))
    file_object = Path(f"{subpath}/" + file_name)
    info_dict["File size"].append(file_object.stat().st_size)
    info_dict["Modification date"].append(
        datetime.fromtimestamp(file_object.stat().st_mtime, tz=pytz.timezone("cet"))
    )
    return info_dict


def dataframe_creation():
    global courses_list, dir_notebook
    info_dict = {
        "File path": [],
        "File name": [],
        "File size": [],
        "Modification date": [],
    }
    for course in courses_list:
        path_object = Path(course.join(dir_notebook))
        for subpath_object in path_object.iterdir():
            subpath = str(subpath_object)
            file_list = notebook_selector(subpath_object)
            for file_name in file_list:
                info_dict = info_collector(course, subpath, file_name, info_dict)
    return pd.DataFrame.from_dict(data=info_dict)


def date_format(time):
    return datetime.fromtimestamp(time, tz=pytz.timezone("cet"))


def alteration_monitor(path_object, cell_time, cell_size):
    global alteration
    for file_object in path_object.iterdir():
        print(file_object)
        if file_object.stat().st_size != cell_size.item():
            cell_time = date_format(file_object.stat().st_mtime)
            cell_size = file_object.stat().st_size
            alteration = True
            return cell_time, cell_size
        else:
            alteration = False
            return cell_time.values[0], cell_size.values[0]


def file_checker(func):
    @wraps(func)
    def wrapper():
        global alteration, courses_list, csv_object, dir_notebook
        compression_recorder_dict = {}
        if csv_object.is_file():
            df = pd.read_csv(csv_object)
            info_dict = df.to_dict("list")
            subpath_recorder = []
            for course in courses_list:
                path_object = Path(course.join(dir_notebook))
                for subpath_object in path_object.iterdir():
                    subpath = str(subpath_object)
                    subpath_recorder.append(subpath)
                    file_list = notebook_selector(subpath_object)
                    for file_name in file_list:
                        if (
                            file_name
                            not in df.loc[df["File path"] == course][
                                "File name"
                            ].to_list()
                        ):
                            info_dict = info_collector(
                                course, subpath, file_name, info_dict
                            )
                            info_dict["Compressed file"].append("")
                            info_dict["Compressed size"].append("")
                            df = pd.DataFrame.from_dict(data=info_dict)
                            index = df.shape[0] - 1
                            compression_recorder_dict[index] = func(
                                f"{subpath}/" + file_name
                            )
                        else:
                            df.loc[
                                (df["File path"] == course)
                                & (df["File name"] == file_name),
                                ["Modification date", "File size"],
                            ] = alteration_monitor(
                                subpath_object,
                                df.loc[
                                    (df["File path"] == course)
                                    & (df["File name"] == file_name),
                                    "Modification date",
                                ],
                                df.loc[
                                    (df["File path"] == course)
                                    & (df["File name"] == file_name),
                                    "File size",
                                ],
                            )
                            if alteration:
                                for index, row in df.iterrows():
                                    if (
                                        subpath
                                        == row["File path"].join(dir_notebook)
                                        + row["File name"].split(".")[0]
                                    ):
                                        compression_recorder_dict[index] = func(
                                            f"{subpath}/" + file_name
                                        )
        else:
            df = dataframe_creation()
            for index, row in df.iterrows():
                subpath = (
                    row["File path"].join(dir_notebook) + row["File name"].split(".")[0]
                )
                compression_recorder_dict[index] = func(
                    subpath + "/" + row["File name"]
                )
        return df, compression_recorder_dict

    return wrapper


def compression_record(func):
    @wraps(func)
    def wrapper():
        global csv_object
        df, compression_recorder_dict = func()
        df["Compressed file"] = ""
        if compression_recorder_dict != {}:
            for key, value in compression_recorder_dict.items():
                df.loc[key, "Compressed file"] = value.split("/")[-1]
                compressed_file_object = Path(value)
                scale = 1
                while compressed_file_object.stat().st_size > 15 * (10**6):
                    compress(value, value, img_width=800 - 40 * scale, img_format="png")
                    scale += 1
                df.loc[key, "Compressed Size"] = compressed_file_object.stat().st_size
                print(
                    datetime.fromtimestamp(
                        compressed_file_object.stat().st_mtime, tz=pytz.timezone("cet")
                    )
                )
                df.loc[key, "Date of Compression"] = datetime.fromtimestamp(
                    compressed_file_object.stat().st_mtime, tz=pytz.timezone("cet")
                )

        df.to_csv(csv_object, index=False)

    return wrapper


@compression_record
@file_checker
def file_generator(original_filename):
    compressed_filename = " (Compressed).ipynb".join(original_filename.split(".ipynb"))
    compress(original_filename, compressed_filename, img_width=800, img_format="png")
    return compressed_filename


alteration = False

courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
    "PyTorch for Deep Learning and Computer Vision",
]

csv_object = Path("modification_record.csv")

dir_notebook = ["./", "/Notebooks/"]

file_generator()
