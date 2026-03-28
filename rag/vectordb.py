from pymongo import MongoClient
from langchain_community.vectorstores import FAISS
from config import MONGODB_URI
import pickle

# MongoDB connection for PDF storage only
try:
    if MONGODB_URI and MONGODB_URI != "your_mongodb_atlas_connection_string_here":
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client['legal_ai_db']
        pdfs_collection = db['pdfs']
        print("✓ MongoDB PDF Storage connected!")
    else:
        pdfs_collection = None
        print("⚠ MongoDB not configured for PDF storage")
except Exception as e:
    print(f"⚠ MongoDB PDF Storage connection failed: {e}")
    pdfs_collection = None


def store_pdf(user_id: str, filename: str, file_data: bytes):
    """Store PDF file in MongoDB"""
    if pdfs_collection is None:
        raise Exception("MongoDB not connected")
    
    # Delete old PDF for this user
    pdfs_collection.delete_many({"user_id": user_id})
    
    # Store new PDF
    pdf_doc = {
        "user_id": user_id,
        "filename": filename,
        "data": file_data
    }
    pdfs_collection.insert_one(pdf_doc)
    print(f"✓ Stored PDF in MongoDB: {filename}")


def get_pdf(user_id: str):
    """Retrieve PDF from MongoDB"""
    if pdfs_collection is None:
        return None
    
    pdf_doc = pdfs_collection.find_one({"user_id": user_id})
    return pdf_doc


def create_vector_db(chunks, embeddings):
    """Create FAISS vector database in memory"""
    db = FAISS.from_documents(chunks, embeddings)
    return db


def load_vector_db(embeddings):
    """This function is not used anymore since we keep FAISS in memory"""
    pass
