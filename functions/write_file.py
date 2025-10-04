import os

from google.genai import types

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
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specified file, constrained to the working directory. Creates any necessary directories.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
