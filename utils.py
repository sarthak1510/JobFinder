# utils.py

import os
from dotenv import load_dotenv

REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "ADZUNA_APP_ID",
    "ADZUNA_API_KEY"
]

def load_environment():
    """
    Loads environment variables from a .env file if it exists.
    Ensures all required keys are present (from .env or actual environment).
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    dotenv_path = os.path.join(project_root, ".env")

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(f"📍 .env loaded from: {dotenv_path}")
    else:
        print("⚠️ .env file not found. Assuming environment variables are set via deployment platform.")

    print("🔐 Loaded Keys:")
    missing = []
    for key in REQUIRED_KEYS:
        val = os.getenv(key)
        print(f" - {key}: {'✅ Loaded' if val else '❌ Not Found'}")
        if not val:
            missing.append(key)

    if missing:
        raise EnvironmentError(f"❌ Missing required environment variables: {', '.join(missing)}")
