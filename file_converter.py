from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import nbformat
import pandas as pd
from pathlib import Path
import pytz


def hidden_file_cleaner(path_object):
    if Path(str(path_object).rstrip("/") + "/.DS_Store").exists():
        path_object = Path(str(path_object).rstrip("/") + "/.DS_Store")
        path_object.unlink()


def date_format(stat_time):
    return datetime.fromtimestamp(stat_time, tz=pytz.timezone("cet"))


def alteration_monitor(file_object, recorded_size, recorded_time):
    global alteration_list
    if file_object.stat().st_mtime != recorded_time.item():
        recorded_size = f"{file_object.stat().st_size:,}"
        recorded_time = str(date_format(file_object.stat().st_mtime))
        alteration = True
        return recorded_size, recorded_time
    else:
        alteration = False
        return recorded_size.item(), recorded_time.item()


def notebook_selector(path_object):
    return [
        file_object.name
        for file_object in sorted(path_object.iterdir())
        if (
            file_object.name.split(".")[-1] == "ipynb"
            and file_object.name.find("(Compressed)") == -1
        )
    ]


def info_collector(course, subpath, file_name, info_dict):
    global dir_notebook
    info_dict["File Path"].append(course)
    info_dict["File Name"].append(file_name)
    path_object = Path(course.join(dir_notebook))
    file_object = Path(f"{subpath}/" + file_name)
    info_dict["File Size"].append(f"{file_object.stat().st_size:,}")
    info_dict["Modification Date"].append(str(date_format(file_object.stat().st_mtime)))
    for key in ["Compressed File", "Compressed Size", "Compressed Date"]:
        info_dict[key].append("")
    return info_dict


def dataframe_creation():
    global courses_list, dir_notebook
    info_dict = {
        "File Path": [],
        "File Name": [],
        "File Size": [],
        "Modification Date": [],
        "Compressed File": [],
        "Compressed Size": [],
        "Compressed Date": [],
    }
    for course in courses_list:
        path_object = Path(course.join(dir_notebook))
        hidden_file_cleaner(path_object)
        for subpath_object in sorted(path_object.iterdir()):
            hidden_file_cleaner(subpath_object)
            subpath = str(subpath_object)
            file_list = notebook_selector(subpath_object)
            for file_name in file_list:
                info_dict = info_collector(course, subpath, file_name, info_dict)
    return pd.DataFrame.from_dict(data=info_dict)


def file_checker(func):
    @wraps(func)
    def wrapper():
        global alteration_list, courses_list, csv_object, dir_notebook
        compression_recorder_dict = {}
        # Condition 1: Check whether there exists a record for all Jupyter Notebook files in
        # the current directory.
        if csv_object.is_file():
            # Condition 2: If Condition 1 is True, read this record and check whether there are
            # certain entries in this record for which the corresponding Jupyter Notebook file
            # cannot be found.
            df = pd.read_csv(csv_object)
            info_dict = df.to_dict("list")
            combined_list = []
            for course in courses_list:
                hidden_file_cleaner(Path(course))
                path_object = Path(course.join(dir_notebook))
                hidden_file_cleaner(path_object)
                for subpath_object in sorted(path_object.iterdir()):
                    combined_list.append((course, subpath_object.name + ".ipynb"))
            for index, row in df.iterrows():
                if (row["File Path"], row["File Name"]) not in combined_list:
                    # Statement 2: If Condition 2 is True, delete those entries and reset the
                    # index.
                    df.drop(axis=0, index=index, inplace=True)
            df.reset_index()
            # Condition 3: If Condition 2 is False, check all Jupyter Notebook files in the
            # current directory one by one to see if that file does not have a corresponding
            # entry in this record.
            for course in courses_list:
                path_object = Path(course.join(dir_notebook))
                for subpath_object in sorted(path_object.iterdir()):
                    hidden_file_cleaner(subpath_object)
                    subpath = str(subpath_object)
                    file_list = notebook_selector(subpath_object)
                    for file_name in file_list:
                        if (
                            file_name
                            not in df.loc[df["File Path"] == course][
                                "File Name"
                            ].to_list()
                        ):
                            info_dict = info_collector(
                                course, subpath, file_name, info_dict
                            )
                            df = pd.DataFrame.from_dict(data=info_dict)
                            index = df.shape[0] - 1
                            compression_recorder_dict[index] = func(
                                f"{subpath}/" + file_name
                            )
                            df = df.sort_values(by=["File Path", "File Name"])
                            df.reset_index()
                        else:
                            for file_object in sorted(subpath_object.iterdir()):
                                df.loc[
                                    (df["File Path"] == course)
                                    & (df["File Name"] == file_name),
                                    ["Modification Date", "File Size"],
                                ] = alteration_monitor(
                                    file_object,
                                    df.loc[
                                        (df["File Path"] == course)
                                        & (df["File Name"] == file_name),
                                        "File Size",
                                    ],
                                    df.loc[
                                        (df["File Path"] == course)
                                        & (df["File Name"] == file_name),
                                        "Modification Date",
                                    ],
                                )

                                """
                                if alteration:
                                    compression_recorder_dict[index] = func(
                                            f"{subpath}/" + file_name
                                        )
                                """
                            """
                            if alteration:
                                for index, row in df.iterrows():
                                    if (
                                        subpath
                                        == row["File Path"].join(dir_notebook)
                                        + row["File Name"].split(".")[0]
                                    ):
                                        compression_recorder_dict[index] = func(
                                            f"{subpath}/" + file_name
                                        )
                                    """
        else:
            # Statement 1: If Condition 1 is False, create a record for all Jupyter Notebook
            # files in the current directory immediately, while generating the corresponding
            # pre-compressed copy for each file as well as compressing any copies that exceed
            # the preset size limit.
            df = dataframe_creation()
            for index, row in df.iterrows():
                subpath = (
                    row["File Path"].join(dir_notebook) + row["File Name"].split(".")[0]
                )
                df.loc[index, "Compressed File"] = func(
                    subpath + "/" + row["File Name"]
                )
        return df

    return wrapper


def compression_record(func):
    @wraps(func)
    def wrapper():
        global csv_object
        df = func()
        if not df.empty:
            for index, row in df.iterrows():
                compressed_file_object = Path(
                    row["File Path"].join(dir_notebook)
                    + row["File Name"].split(".")[0]
                    + "/"
                    + row["Compressed File"]
                )
                scale = 1
                while compressed_file_object.stat().st_size > 15 * (10**6):
                    compressed_file_path = str(compressed_file_object)
                    original_file_path = ".ipynb".join(
                        compressed_file_path.split(" (Compressed).ipynb")
                    )
                    compress(
                        original_file_path,
                        compressed_file_path,
                        img_width=800 - 40 * scale,
                        img_format="png",
                    )
                    scale += 1
                df.loc[index, "Compressed Size"] = (
                    f"{compressed_file_object.stat().st_size:,}"
                )
                df.loc[index, "Compressed Date"] = str(
                    date_format(compressed_file_object.stat().st_mtime)
                )

        df.to_csv(csv_object, index=False)

    return wrapper


@compression_record
@file_checker
def file_generator(original_file_path):
    compressed_file_path = " (Compressed).ipynb".join(
        original_file_path.split(".ipynb")
    )
    compress(original_file_path, compressed_file_path, img_width=800, img_format="png")
    return compressed_file_path.split("/")[-1]


alteration = False

courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
    "PyTorch for Deep Learning and Computer Vision",
]

csv_object = Path("modification_record.csv")

dir_notebook = ["./", "/Notebooks/"]

file_generator()
