import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(working_directory):
        raise ValueError(f"Error: cannot access {file_path} as it is outside the working directory")
    if not os.path.exists(full_path):
        raise ValueError(f"Error: file {file_path} does not exist")
    if not os.path.isfile(full_path):
        raise ValueError(f"Error: {file_path} is not a file")

    final_response = ""

    try:
        with open(full_path, "r") as f:
            content = f.read(MAX_CHARS)
            final_response += f"Content of {file_path}:\n{content}\n"
    except Exception as e:
        final_response += f"Error: reading {file_path}: {str(e)}\n"

    return final_response
