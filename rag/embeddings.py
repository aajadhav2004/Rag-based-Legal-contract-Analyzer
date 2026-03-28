from langchain_huggingface import HuggingFaceInferenceAPIEmbeddings
from config import HF_TOKEN

def load_embeddings():
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HF_TOKEN,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings
