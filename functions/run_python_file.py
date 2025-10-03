import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # validate full path stays within working directory
    if not os.path.commonpath([working_directory, full_path]) == working_directory:
        raise ValueError(f"Error: cannot run {file_path} as it is outside the working directory")   
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise ValueError(f"Error: {file_path} does not exist or is not a file")
    
    command = ["python3", full_path] + args
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output_parts.append(f"Error: Process exited with code {result.returncode}")
        if not output_parts:
            return "Error: No output produced."
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"