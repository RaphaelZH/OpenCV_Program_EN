from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import os
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


def file_checker(func):
    @wraps(func)
    def wrapper():
        global courses_list, csv_object, dir_notebook
        output_filename_dict = {}
        if csv_object.is_file():
            df = pd.read_csv(csv_object)
            info_dict = df.to_dict("list")
            for course in courses_list:
                path_object = Path(course.join(dir_notebook))
                path_counter = len(list(notebook_selector(path_object)))
                if path_counter != len(df.loc[df["File path"] == course]):
                    for file in notebook_selector(path_object):
                        input_filename = Path(course.join(dir_notebook) + file)
                        file_object = Path(input_filename)
                        if file not in df.loc[df["File path"] == course]["File name"]:
                            info_dict = info_collector(course, file, info_dict)
                            #df = pd.DataFrame.from_dict(data=info_dict)
                            
                        print(date_format(file_object.stat().st_mtime))
                        """
                        elif (
                            date_format(file_object.stat().st_mtime)
                            != df.loc[
                                df["File path"] == course and df["File name"] == file
                            ]["Modification date"]
                            and file_object.stat().st_size
                            != df.loc[
                                df["File path"] == course and df["File name"] == file
                            ]["File size"]
                        ):
                            df.loc[
                                df["File path"] == course and df["File name"] == file
                            ]["Modification date"] = date_format(
                                file_object.stat().st_mtime
                            )
                            df.loc[
                                df["File path"] == course and df["File name"] == file
                            ]["File size"] = file_object.stat().st_size
                        """
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
        if output_filename_dict != {}:
            for index, (key, value) in zip(df.index, output_filename_dict.items()):
                if index == key:
                    df.loc[index, "Compressed file"] = value.split("/Notebooks/")[-1]
                    file_object = Path(value)
                    df.loc[index, "Compressed size"] = file_object.stat().st_size
        df.to_csv(csv_object, index=False)

    return wrapper


@compression_record
@file_checker
def file_generator(input_filename):
    os.system(f"jupyter nbconvert --to html '{input_filename}'")
    output_filename = " (Compressed).ipynb".join(input_filename.split(".ipynb"))
    compress(input_filename, output_filename, img_width=800, img_format="png")
    return output_filename


courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
]

csv_object = Path("modification_record.csv")

dir_notebook = ["./", "/Notebooks/"]

file_generator()
