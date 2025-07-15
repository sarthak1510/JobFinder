# utils.py

import os
from dotenv import load_dotenv

REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "ADZUNA_APP_ID",
    "ADZUNA_API_KEY"
]

def load_environment():
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    dotenv_path = os.path.join(project_root, ".env")

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"❌ .env file not found at: {dotenv_path}")

    load_dotenv(dotenv_path)

    print(f"📍 .env loaded from: {dotenv_path}")
    print("🔐 Loaded Keys:")
    for key in REQUIRED_KEYS:
        val = os.getenv(key)
        print(f" - {key}: {'✅ Loaded' if val else '❌ Not Found'}")

    
    missing = [key for key in REQUIRED_KEYS if not os.getenv(key)]
    if missing:
        raise EnvironmentError(f"❌ Missing keys in .env: {', '.join(missing)}")
