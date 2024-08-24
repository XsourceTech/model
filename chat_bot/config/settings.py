import os
from pathlib import Path

# load the environment variables from the .env file
try:
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except ImportError:
    pass


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_BASE = os.getenv("MISTRAL_BASE")
MISTRAL_KEY = os.getenv("MISTRAL_KEY")
