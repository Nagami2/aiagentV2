# aiagentV2

Lightweight AI coding-agent demo built around the Google GenAI tools. This repository contains small helper functions that allow the agent to list files, read files, run Python files, and write files inside a constrained working directory.

## What this project contains

- `main.py` — example entry point that runs the agent loop using the Google GenAI SDK.
- `call_function.py` — helper to dispatch tool calls returned by the model.
- `functions/` — small helper functions exposed to the agent:
	- `get_files_info.py` — list files in a directory (restricted to the working directory).
	- `get_file_content.py` — read file contents.
	- `write_file.py` — write (and create) files under the working directory.
	- `run_python_file.py` — run a python file and capture output.
- `calculator/` — a tiny example package with a `Calculator` class and tests.

## Quick start

Prerequisites: Python 3.9+ (recommended 3.11+), and a virtual environment.

On macOS with Homebrew you can create a clean Python via pyenv. Use `uv` to install dependencies and run scripts in the venv context.

```bash
brew install pyenv
pyenv install 3.11.6
pyenv local 3.11.6
python -m venv .venv
source .venv/bin/activate
uv install -r requirements.txt  # if present
```

Run the main demo with `uv`:

```bash
uv run main.py "list files"
```

Run the calculator tests with `uv`:

```bash
uv run python calculator/tests.py
```

## Notes and tips

- The helper functions in `functions/` are intentionally constrained to the repo working directory for safety. They use absolute path checks — callers should pass paths relative to the working directory (or the function can be updated to handle absolute paths safely).
- `write_file` will create missing parent directories and will create or overwrite the target file (mode `w`). If you want to avoid overwriting, change the mode to `x`.
- If you see unexpected files (for example `calculator/calculator/lorem.txt`) that typically means the caller supplied a `working_directory` and a `file_path` that combined to duplicate the directory segment; pass `file_path` relative to the `working_directory` to avoid this.

