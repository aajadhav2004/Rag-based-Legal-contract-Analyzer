import shutil
from langchain_community.vectorstores import FAISS
from config import VECTOR_DB_PATH


def create_vector_db(chunks, embeddings):

    # delete old vectordb
    shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)

    db = FAISS.from_documents(chunks, embeddings)

    db.save_local(VECTOR_DB_PATH)

    return db


def load_vector_db(embeddings):

    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db