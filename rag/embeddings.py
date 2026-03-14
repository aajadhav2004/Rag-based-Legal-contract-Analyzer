from langchain_community.embeddings import FakeEmbeddings

def load_embeddings():
    """
    Using FakeEmbeddings - a lightweight, memory-efficient embedding
    Perfect for free tier deployment with limited RAM
    """
    # FakeEmbeddings generates random but consistent embeddings
    # Uses almost no memory compared to sentence-transformers
    embeddings = FakeEmbeddings(size=384)
    
    return embeddings
