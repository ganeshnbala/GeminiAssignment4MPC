import os
from dotenv import load_dotenv

# Load environment variables from config.env file
load_dotenv('config.env')

# Check what we're getting
api_key = os.getenv("GEMINI_API_KEY")
print(f"Raw API key: '{api_key}'")
print(f"API key length: {len(api_key) if api_key else 'None'}")
print(f"API key type: {type(api_key)}")

# Check for any hidden characters
if api_key:
    print(f"API key bytes: {api_key.encode('utf-8')}")
    print(f"API key starts with: '{api_key[:10]}...'")
    print(f"API key ends with: '...{api_key[-10:]}'")

# Also check environment variables directly
print(f"\nDirect env check: {os.environ.get('GEMINI_API_KEY')}")
