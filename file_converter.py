from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import pandas as pd
from pathlib import Path
import pytz


def notebook_selector(path_object):
    return [
        file.name
        for file in path_object.iterdir()
        if (
            file.name.split(".")[-1] == "ipynb" and file.name.find("(Compressed)") == -1
        )
    ]


def info_collector(course, file, info_dict):
    global dir_notebook
    info_dict["File path"].append(course)
    info_dict["File name"].append(file)
    file_object = Path(course.join(dir_notebook) + file)
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
        file_list = notebook_selector(path_object)
        for file in file_list:
            info_dict = info_collector(course, file, info_dict)
    return pd.DataFrame.from_dict(data=info_dict)


def date_format(time):
    return datetime.fromtimestamp(time, tz=pytz.timezone("cet"))


def alteration_monitor(file_object, cell_time, cell_size):
    global alteration
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
        output_filename_dict = {}
        if csv_object.is_file():
            df = pd.read_csv(csv_object)
            info_dict = df.to_dict("list")
            for course in courses_list:
                path_object = Path(course.join(dir_notebook))
                for file in notebook_selector(path_object):
                    input_filename = course.join(dir_notebook) + file
                    file_object = Path(input_filename)
                    if (
                        file
                        not in df.loc[df["File path"] == course]["File name"].to_list()
                    ):
                        info_dict = info_collector(course, file, info_dict)
                        info_dict["Compressed file"].append("")
                        info_dict["Compressed size"].append("")
                        df = pd.DataFrame.from_dict(data=info_dict)
                        index = df.shape[0] - 1
                        output_filename_dict[index] = func(input_filename)
                    else:
                        df.loc[
                            (df["File path"] == course) & (df["File name"] == file),
                            ["Modification date", "File size"],
                        ] = alteration_monitor(
                            file_object,
                            df.loc[
                                (df["File path"] == course) & (df["File name"] == file),
                                "Modification date",
                            ],
                            df.loc[
                                (df["File path"] == course) & (df["File name"] == file),
                                "File size",
                            ],
                        )
                        if alteration:
                            for index, row in df.iterrows():
                                if (
                                    input_filename
                                    == row["File path"].join(dir_notebook)
                                    + row["File name"]
                                ):
                                    output_filename_dict[index] = func(input_filename)
        else:
            df = dataframe_creation()
            for index, row in df.iterrows():
                input_filename = row["File path"].join(dir_notebook) + row["File name"]
                output_filename_dict[index] = func(input_filename)
        return df, output_filename_dict

    return wrapper


def compression_record(func):
    @wraps(func)
    def wrapper():
        global csv_object
        df, output_filename_dict = func()
        df["Compressed file"] = ""
        df["Compressed file"].astype("object")
        if output_filename_dict != {}:
            for key, value in output_filename_dict.items():
                df.loc[key, "Compressed file"] = value.split("/Notebooks/")[-1]
                file_object = Path(value)
                df.loc[key, "Compressed size"] = file_object.stat().st_size
        df.to_csv(csv_object, index=False)

    return wrapper


@compression_record
@file_checker
def file_generator(input_filename):
    output_filename = " (Compressed).ipynb".join(input_filename.split(".ipynb"))
    compress(input_filename, output_filename, img_width=800, img_format="png")
    return output_filename


alteration = False

courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
]

csv_object = Path("modification_record.csv")

dir_notebook = ["./", "/Notebooks/"]

file_generator()
