from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-flash-latest"

UPLOAD_DIR = "uploads"
EXTRACTED_DIR = "extracted"
GENERATED_DIR = "generated"