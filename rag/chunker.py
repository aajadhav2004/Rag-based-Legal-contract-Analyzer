from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_docs(docs, max_chunks=100):
    """Split documents with memory limit for Render free tier (512MB)"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)
    
    # Limit chunks to prevent memory issues on free tier
    if len(chunks) > max_chunks:
        print(f"⚠️ Limiting chunks from {len(chunks)} to {max_chunks} for memory safety")
        chunks = chunks[:max_chunks]

    return chunks