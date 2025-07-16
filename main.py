
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info

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

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
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
    if response.function_calls:
        for r in response.function_calls:
            print (f"Calling function: {r.name}({r.args})")
   # else:
       # print(response.text)
    if verbose == True:
    
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)
    

    
   # print(user_input)
    
   



if __name__ == "__main__":
    main()