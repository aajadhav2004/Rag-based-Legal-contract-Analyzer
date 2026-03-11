from rag.analyzer import generate


def ask_question(db, question, filename="contract.pdf"):
    """
    Answer questions using STRICT RAG with source citations
    Returns answer with page numbers and source paragraphs
    """
    
    # Retrieve relevant documents
    docs = db.similarity_search(question, k=5)
    
    if not docs:
        return {
            "answer": "The contract does not explicitly mention this information.",
            "sources": []
        }
    
    # Build context with page numbers
    context_parts = []
    for i, doc in enumerate(docs):
        page = doc.metadata.get('page', 'Unknown')
        context_parts.append(f"[Source {i+1} - Page {page}]\n{doc.page_content}")
    
    context = "\n\n".join(context_parts)
    
    # Strict RAG prompt
    prompt = f"""You are a legal contract analyst. Answer the question using ONLY the provided contract text.

IMPORTANT RULES:
1. Answer ONLY based on the contract text provided below
2. If the answer is not in the contract, respond: "The contract does not explicitly mention this information."
3. Cite the page number in your answer
4. Be precise and factual

Contract Context:
{context}

Question: {question}

Answer (include page references):"""

    answer = generate(prompt)
    
    # Build sources list
    sources = []
    for doc in docs:
        sources.append({
            "page": doc.metadata.get('page', 'Unknown'),
            "text": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
            "filename": filename
        })
    
    return {
        "answer": answer,
        "sources": sources
    }
