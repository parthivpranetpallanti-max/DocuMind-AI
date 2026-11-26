import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-3.8-flash"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

STORAGE_DIR = "storage"
UPLOAD_DIR = "uploaded_documents"

os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)