import os
def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
    
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        directory = os.path.dirname(file_path_abs)
        os.makedirs(directory, exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return (f"Error:  {e}")