
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

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
    - Write or overwite files"

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content]
    )
    config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
    user_input = sys.argv[1]
    
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=user_input,
    config=config,
)
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Calling function: {function_call.name}({dict(function_call.args)})")
    else:
       print(response.text)
    if verbose == True:
    
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    #else:
       # print(response.text)
    

    
   # print(user_input)
    
   



if __name__ == "__main__":
    main()