import os
from ipynbcompress import compress

import os, sys

from datetime import datetime, timezone

from pathlib import Path

courses_list = ["Deep Learning with PyTorch for Medical Image Analysis", "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4"]

dir_notebook = ["/", "/Notebooks/"]

for course in courses_list:
    print(dir_notebook.join(course))
"""
path_object = Path(dir_path)
dir_path = "../Datasets/Kaggle - CT Medical Images/dicom_dir/"
"""

"""
    [
        file.name
        for file in path_object.iterdir()
        if (
            file.is_file()
            and pydicom.read_file(dir_path + file.name).BodyPartExamined != "CHEST"
        )
    ]
)
"""
#input_filename = "2 - CNN - Convolutional Neural Networks.ipynb"

# Showing stat information of file
#stinfo = os.stat(input_filename)
#print(stinfo)

# Using os.stat to recieve atime and mtime of file
#print("access time of .py: %s" %datetime.fromtimestamp(stinfo.st_atime))
#print("modified time of .py: %s" %datetime.fromtimestamp(stinfo.st_mtime))

"""

input_filename = "2 - CNN - Convolutional Neural Networks.ipynb"

#os.system(f"jupyter nbconvert --to notebook --execute '{input_filename}'")
#os.system(f"jupyter nbconvert --to notebook --inplace '{input_filename}'")
os.system(f"jupyter nbconvert --to html '{input_filename}'")

"""



"""
output_filename = " (Compressed).".join(input_filename.split("."))

print(os.stat(input_filename).st_size)

# Keep the original file and create another compressed file to upload to GitHub by
# specifying the width of the output image
compress(
    input_filename, output_filename=output_filename, img_width=800, img_format="png"
)

print(os.stat(output_filename).st_size)
"""