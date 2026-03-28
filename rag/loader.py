from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import io
from pypdf import PdfReader

def load_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    return docs


def load_pdf_from_bytes(file_data: bytes, filename: str):
    """Load PDF from bytes data (for MongoDB storage)"""
    pdf_file = io.BytesIO(file_data)
    pdf_reader = PdfReader(pdf_file)
    
    docs = []
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        doc = Document(
            page_content=text,
            metadata={"page": page_num + 1, "source": filename}
        )
        docs.append(doc)
    
    return docs
