import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        #file_path = os.path.abspath(file_path)
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        new_file_content_string = file_content_string
        if os.path.getsize(file_path_abs) > MAX_CHARS:
            new_file_content_string = file_content_string + (f'[...File "{file_path}" truncated at 10000 characters]')
        return new_file_content_string
    except Exception as e:
        return (f"Error:  {e}")
