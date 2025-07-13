import os

def get_files_info(working_directory, directory=None):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        directory = os.path.join(working_directory, directory) if directory else working_directory
        directory = os.path.abspath(directory)

        # Guard: ensure directory is within working_directory
        if not os.path.commonpath([working_directory, directory]) == working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Guard: ensure it's a directory
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        # Build result string
        result_lines = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                result_lines.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                result_lines.append(f'- {item}: Error retrieving info: {e}')

        return "\n".join(result_lines)

    except Exception as e:
        return f'Error: {e}'
