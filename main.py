import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Schemas for the AI to read:
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

# Functions for the AI to use:
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

# Load .env variables
load_dotenv()

# Get the API key from environment
api_key = os.environ.get("GEMINI_API_KEY")

# Now you can use the key
client = genai.Client(api_key=api_key)


def main():
    verbose = False

    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    if len(sys.argv) < 2:
        print("No input provided.")
        sys.exit(1)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )

    user_input = sys.argv[1]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=user_input,
        config=config,
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call

        # Call the function
        function_call_result = call_function(function_call, verbose)

        # Sanity check
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Something went wrong, try using --verbose to find out what")

        # Print result if verbose
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    # Handle verbose printing first
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Maps strings to Functions
    function_map = {
        "write_file": write_file,
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
    }

    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    # Add working directory to arguments
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    result = function_map[function_call_part.name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )


if __name__ == "__main__":
    main()



