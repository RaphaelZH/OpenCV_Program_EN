import os
from ipynbcompress import compress

import os, sys

from datetime import datetime, timezone

input_filename = "2 - CNN - Convolutional Neural Networks.ipynb"

# Showing stat information of file
stinfo = os.stat(input_filename)
print(stinfo)

# Using os.stat to recieve atime and mtime of file
print("access time of a2.py: %s" %datetime.fromtimestamp(stinfo.st_atime))
print("modified time of a2.py: %s" %datetime.fromtimestamp(stinfo.st_mtime))

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