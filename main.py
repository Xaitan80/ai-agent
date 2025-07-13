import os
from dotenv import load_dotenv
from google import genai
import sys

# Load .env variables
load_dotenv()

# Get the API key from environment
api_key = os.environ.get("GEMINI_API_KEY")

# Now you can use the key
client = genai.Client(api_key=api_key)



def main():
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)
    print(response.text)
    
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    if len(sys.argv) < 2:
        print("No input provided.")
        sys.exit(1)

    user_input = sys.argv[1]
    print(user_input)



if __name__ == "__main__":
    main()
