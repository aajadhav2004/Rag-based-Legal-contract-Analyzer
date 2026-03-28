import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

# Note: UPLOAD_FOLDER and VECTOR_DB_PATH are no longer needed
# PDFs are stored in MongoDB, vectors are stored in FAISS (in-memory)