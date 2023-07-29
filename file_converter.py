from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import os
import pandas as pd
from pathlib import Path
import pytz


def dataframe_creation():
    global courses_list
    dir_notebook = ["./", "/Notebooks/"]
    file_name_list = []
    file_path_list = []
    st_size_list = []
    st_mtime_list = []
    for course in courses_list:
        path_object = Path(course.join(dir_notebook))
        for file in path_object.iterdir():
            if (
                file.name.split(".")[-1] == "ipynb"
                and file.name.find("(Compressed)") == -1
            ):
                file_path_list.append(course.join(dir_notebook))
                file_name_list.append(file.name)
                file_object = Path(course.join(dir_notebook) + file.name)
                st_size_list.append(file_object.stat().st_size)
                st_mtime_list.append(
                    datetime.fromtimestamp(
                        file_object.stat().st_mtime, tz=pytz.timezone("cet")
                    )
                )
    return pd.DataFrame(
        list(zip(file_path_list, file_name_list, st_size_list, st_mtime_list)),
        columns=["File path", "File name", "File size", "Modification date"],
    )


def file_checker(func):
    @wraps(func)
    def wrapper():
        global csv_file
        if csv_file.is_file():
            df = pd.read_csv(csv_file)
            for index, row in df.iterrows():
                input_filename = row["File path"] + row["File name"]
                file_object = Path(input_filename)
                if (
                    datetime.fromtimestamp(
                        file_object.stat().st_mtime, tz=pytz.timezone("cet")
                    )
                    != row["Modification date"]
                    and file_object.stat().st_size != row["File size"]
                ):
                    df.loc[index, "Modification date"] = datetime.fromtimestamp(
                        file_object.stat().st_mtime, tz=pytz.timezone("cet")
                    )
                    output_filename = func(input_filename)
                    df.loc[index, "Compressed file"] = output_filename.split(
                        "/Notebooks/"
                    )[-1]
                    file_object = Path(output_filename)
                    df.loc[index, "Compressed size"] = file_object.stat().st_size
        else:
            df = dataframe_creation()
            for index, row in df.iterrows():
                input_filename = row["File path"] + row["File name"]
                output_filename = func(input_filename)
                df.loc[index, "Compressed file"] = output_filename.split("/Notebooks/")[
                    -1
                ]
                file_object = Path(output_filename)
                df.loc[index, "Compressed size"] = file_object.stat().st_size
        df.to_csv(csv_file, index=False)

    return wrapper


@file_checker
def file_generator(input_filename):
    os.system(f"jupyter nbconvert --to html '{input_filename}'")
    output_filename = " (Compressed).ipynb".join(input_filename.split(".ipynb"))
    compress(
        input_filename, output_filename=output_filename, img_width=800, img_format="png"
    )
    return output_filename


courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
]

csv_file = Path("modification_record.csv")

file_generator()
