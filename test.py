import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", api_key is not None)

if api_key:
    print("First 8 characters:", api_key[:8])
else:
    print("API key not found.")