import os
from dotenv import load_dotenv
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from openai import OpenAI
import argparse
from prompts import system_prompt
import json

available_functions = [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found!")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):

        response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
        )
        if response.usage == None:
            raise RuntimeError("API request failed!")
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")


        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls != None:
            for tool_call in message.tool_calls:

                result_message = call_function(tool_call)
                #if result_message == None:
                #    raise ValueError("Empty function return!")
                messages.append(result_message)
        else:
            print(f"-> {message.content}")
            return



    return "Maximum number of iterations reached!"
    sys.exit(1)

if __name__ == "__main__":
    main()
