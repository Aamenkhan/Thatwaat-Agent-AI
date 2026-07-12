import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
VOICES_DIR = os.path.join(BASE_DIR, "voices")

# Model settings
OLLAMA_MODEL = "qwen2.5-coder:3b"

# API Keys (Placeholders)
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
