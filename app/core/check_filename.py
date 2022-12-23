import os
import re

def validate_file_name(file_name: str):
    # Check if the file name is a valid JPG or PNG file name
    if not re.match(r"^[\w\d-]+\.(jpg|png)$", file_name, re.IGNORECASE):
        return False

    # Check if the file name contains any slashes or directories
    if "/" in file_name or "\\" in file_name:
        return False

    return True
