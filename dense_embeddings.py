"""
might have to change unique ID calc
"""
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from aggregate_documents import DATA_PATH, CHROMA_PATH
from datetime import datetime

# must change this for non PDF data
def load_pdf_documents():
    # For PDFs in a directory (default behavior):
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def load_slack_documents(messages):
    documents = []
    for message in messages:
        documents.append(Document(page_content=message['text'], metadata={"source": "slack", "page": message['timestamp'], "time": message['datetime']}))
    return documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        length_function=len,
    )

    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)
    print(chunks_with_ids)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if ("time" not in chunk.metadata):
            chunk.metadata["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks) > 0:
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def pdf_pipeline():
    documents = load_pdf_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def slack_pipeline(messages):
    documents = load_slack_documents(messages)
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def remove_all():
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    existing_items = db.get(include=[])
    existing_ids = existing_items["ids"]

    db.delete(ids=existing_ids)


def dense_relevant_documents(query: str, num_docs: int):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search(query=query, k=num_docs)

    return results


if __name__ == "__main__":
    pdf_pipeline()