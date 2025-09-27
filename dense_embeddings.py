"""
might have to change unique ID calc
"""
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from aggregate_documents import DATA_PATH, CHROMA_PATH, TERMINAL_LOG_PATH, GIT_PR_PATH
from datetime import datetime
import asyncio
from curate import get_documentation_suggestions
from supabase_client import execute_documentation_changes
import os
import json
from dotenv import load_dotenv

load_dotenv()

ORION_HOME = os.getenv("ORION_HOME")


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

def load_terminal_documents():
    document_loader = DirectoryLoader(TERMINAL_LOG_PATH)
    return document_loader.load()

def load_github_prs():
    for fname in os.listdir(f"{ORION_HOME}/{GIT_PR_PATH}"):
        if fname.endswith("refined_pr_info.json"):
            filepath = os.path.join(f"{ORION_HOME}/{GIT_PR_PATH}", fname)
            break
    else:
        raise FileNotFoundError("No file ending with refined_pr_info.json found")

    with open(filepath, "r") as file:
        data = json.load(file)
        documents = []
        for pr in data:
            
            
            documents.append(Document(page_content=pr.get('pr_body', "") + pr.get('diff', ""), metadata={"source": "github", "page": f"{pr['pr_number']}{pr['created_at']}", "time":pr['created_at']}))
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

def llm_curation(chunks: list[Document]):
    """
    Gets documentation change suggestions from an LLM and executes them.
    """
    print(f"Starting LLM curation for {len(chunks)} chunks...")
    
    # Get SQL query suggestions from the LLM
    queries = asyncio.run(get_documentation_suggestions(chunks))
    
    if not queries:
        print("LLM Curation: No documentation changes suggested.")
        return

    print(f"LLM Curation: Received {len(queries)} SQL queries to execute.")
    print("--- QUERIES ---")
    for q in queries:
        print(q)
    print("-----------------")

    # Execute the suggested SQL queries
    print("Executing documentation changes...")
    results = execute_documentation_changes(queries)
    
    print("--- EXECUTION RESULTS ---")
    success_count = 0
    error_count = 0
    for result in results:
        print(f"Query: {result['query']}")
        print(f"Status: {result['status']}")
        if result['status'] == 'error':
            error_count += 1
            print(f"Details: {result['details']}")
        else:
            success_count += 1
        print("-" * 10)
    
    print(f"LLM Curation finished. {success_count} queries succeeded, {error_count} failed.")


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
    try:
        llm_curation(documents)
    except:
        print("Curation failed.")

def slack_pipeline(messages):
    documents = load_slack_documents(messages)
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    try:
        llm_curation(documents)
    except:
        print("Curation failed")

def terminal_pipeline():
    documents = load_terminal_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def git_pr_pipeline():
    documents = load_github_prs()
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
    git_pr_pipeline()