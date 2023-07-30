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
            file.name.split(".")[-1] == "ipynb"
            and file.name.find("(Compressed)") == -1
        )
    ]

def dataframe_creation():
    global courses_list
    dir_notebook = ["./", "/Notebooks/"]
    file_name_list = []
    file_path_list = []
    st_size_list = []
    st_mtime_list = []
    for course in courses_list:
        path_object = Path(course.join(dir_notebook))
        file_list = notebook_selector(path_object)
        for file in file_list:
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
        global csv_object
        output_filename_dict = {}
        if csv_object.is_file():
            df = pd.read_csv(csv_object)
            #if 
            #folder counterobject
            for index, row in df.iterrows():
                input_filename = row["File path"] + row["File name"]
                folder_object = Path(row["File path"])
                folder_counter = len([file for file in notebook_selector(folder_object)])
                row_counter = len(df.loc[df["File path"] == row["File path"]])
                if folder_counter != row_counter:
                    print(folder_counter)
                
                
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
                    output_filename_dict[index] = func(input_filename)
        else:
            df = dataframe_creation()
            for index, row in df.iterrows():
                input_filename = row["File path"] + row["File name"]
                output_filename_dict[index] = func(input_filename)
        return df, output_filename_dict

    return wrapper


def compression_record(func):
    @wraps(func)
    def wrapper():
        global csv_object
        df, output_filename_dict = func()
        if output_filename_dict != {}:
            for (index, _), (key, value) in zip(
                df.iterrows(), output_filename_dict.items()
            ):
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
    compress(
        input_filename, output_filename=output_filename, img_width=800, img_format="png"
    )
    return output_filename


courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
]

csv_object = Path("modification_record.csv")

file_generator()
