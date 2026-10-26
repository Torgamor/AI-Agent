import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if  os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args != None:
            for e in args:
                command.extend(e)
        ComProcess = subprocess.run(command, text=True,timeout=30, capture_output=True, cwd=working_dir_abs)
        output = ""
        if ComProcess.returncode != 0:
            output += "Process exited with code X\n"
        if ComProcess.stdout == "" and ComProcess.stderr == "":
            output += "No output produced"
        else:
            output += f"STDOUT: {ComProcess.stdout}\nSTDERR: {ComProcess.stderr}"
        return output




    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "This function executes a python .py file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
                "args": {
                    "type": "list",
                    "description": "Contains the arguments for the function as a python list of strings",
                },
            },
        },
    },
}
