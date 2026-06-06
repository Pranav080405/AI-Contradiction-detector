import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Updated to the correct available model identifier
    MODEL_NAME = "gemini-2.5-flash"