import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(working_directory):
        raise ValueError(f"Error: cannot access {file_path} as it is outside the working directory")
    
    dir_name = os.path.dirname(full_path)
    # create directories if they do not exist
    os.makedirs(dir_name, exist_ok=True)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}. Written {len(content)} characters\n"
    except Exception as e:
        return f"Error: writing to {file_path}: {str(e)}\n"
