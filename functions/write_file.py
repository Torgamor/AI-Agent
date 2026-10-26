import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if  os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isdir(target_file) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        file = open(target_file, mode="w")
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes into a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Contains the content to be inserted into the file",
                },
            },
        },
    },
}
