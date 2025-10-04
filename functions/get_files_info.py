import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    if not full_path.startswith(working_directory):
        raise ValueError(f"Error: cannot list {directory} as it is outside the working directory")
    if not os.path.exists(full_path):
        raise ValueError(f"Error: directory {directory} does not exist")
    if not os.path.isdir(full_path):
        raise ValueError(f"Error: {directory} is not a directory")
    
    final_response = ""

    contents = os.listdir(full_path)
    for content in contents:
        content_path = os.path.join(full_path, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir} \n"
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
