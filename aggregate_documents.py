from langchain.schema import Document
from langchain_community.vectorstores.chroma import Chroma
from embedding_function import get_embedding_function

DATA_PATH = "data"

TERMINAL_LOG_PATH = "oterm/logs"

CHROMA_PATH = "chroma"

LLM_MODEL = "llama3"

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def total_documents():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    return len(db.get(include=[])['ids'])


def get_all_documents():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    data = db.get(include=['metadatas', 'documents'])
    total = total_documents()

    docs = []
    for i in range(total):
        content = data['documents'][i]
        metadata = data['metadatas'][i]
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)

    return docs