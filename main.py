
import sys

import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import get_files_info

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

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    if verbose_flag:
        print(f"Response: {response.text}")
        print(f"Prompt Token Count: {response.usage_metadata.prompt_token_count}")
        print(f"Response Token Count: {response.usage_metadata.candidates_token_count}")

    else:
        print(f"Response: {response.text}")


print(get_files_info("calculator", "bin"))

# if __name__ == "__main__":
#     main()
