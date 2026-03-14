from langchain_huggingface import HuggingFaceEmbeddings

def load_embeddings():
    """
    Using a smaller, lightweight embedding model
    all-MiniLM-L6-v2 is only ~80MB and uses minimal RAM
    Perfect for free tier deployment
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Force CPU usage
        encode_kwargs={'normalize_embeddings': True}  # Better performance
    )
    
    return embeddings
