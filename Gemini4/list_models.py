import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from config.env file
load_dotenv('config.env')

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")

if api_key:
    genai.configure(api_key=api_key)
    
    try:
        # List available models
        models = genai.list_models()
        print("\nAvailable models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
            else:
                print(f"❌ {model.name} (no generateContent support)")
                
    except Exception as e:
        print(f"❌ Error listing models: {e}")
else:
    print("❌ No API key found in config.env")
