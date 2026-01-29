import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

API_KEY = os.getenv("API_KEY", "changeme")
APP_NAME = "Agentic HoneyPot"

# Mistral API
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY not set in environment")

LLM_CLIENT = Mistral(api_key=MISTRAL_API_KEY)
