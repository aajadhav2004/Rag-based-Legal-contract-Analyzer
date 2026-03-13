from langchain_huggingface import HuggingFaceEmbeddings

def load_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
    )

    return embeddings