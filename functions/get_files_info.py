import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.isdir(target_dir) == False:
            return f'Error: "{target_dir}" is not a directory'
        if  os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        directory_items = os.listdir(target_dir)
        return_string = []
        for e in directory_items:
            item_path = os.path.join(target_dir, e)
            if os.path.isdir(item_path) == True:
                isDir = True
            else:
                isDir = False
            return_string.append(f"- {e}: file_size={os.path.getsize(item_path)} bytes, is_dir={isDir}")
        return "\n".join(return_string)




    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
