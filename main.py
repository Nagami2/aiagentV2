
import sys

import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

from call_function import call_function

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <your prompt>")
        sys.exit(1)

    user_prompt = sys.argv[1]

    verbose_flag = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose_flag = True

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    when the user asks about the code project, they are referring to the working directory.
    So, you should typically start by looking at the project's files, and figuring out how to run the project and how to run its tests.
    you will always want to test the tests and actual project to verify that the behaviour is working.
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,  
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    for _ in range(20):
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],            
                system_instruction=system_prompt),
        )

        if response is None or response.usage_metadata is None:
            print("Error: response is malformed or missing usage metadata")
            return
        
        # if verbose_flag:
        #     print(f"User prompt: {user_prompt}")
        #     print(f"Prompt Token Count: {response.usage_metadata.prompt_token_count}")
        #     print(f"Response Token Count: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose_flag)
                # if function_call_result.parts[0].function_response.response:
                #     print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            # final agent text message
            print(f"Response: {response.text}")
            return 


if __name__ == "__main__":
    main()
