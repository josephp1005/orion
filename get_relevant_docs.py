from dense_embeddings import dense_relevant_documents
from sparse_embeddings import sparse_relevant_documents
from grade_documents import grade
from rank_documents import rank_docs
import time


def get_docs(query_text: str):
    start = time.time()
    dense_results = dense_relevant_documents(query_text, 5)
    end = time.time()
    time_dense = end - start

    start = time.time()
    sparse_results = sparse_relevant_documents(query_text, 5)
    end = time.time()
    time_sparse = end - start

    if len(dense_results) == 0 and len(sparse_results) == 0:
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    start = time.time()
    relevant_dense_documents, irrelevant_dense_documents = grade(dense_results, query_text)
    end = time.time()
    time_relevant_dense = end - start

    start = time.time()
    relevant_sparse_documents, irrelevant_sparse_documents = grade(sparse_results, query_text)
    end = time.time()
    time_relevant_sparse = end - start

    if len(relevant_dense_documents) == 0 and len(relevant_sparse_documents):
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    all_documents = []
    for document in relevant_sparse_documents:
        all_documents.append(document)

    for document in relevant_dense_documents:
        found = False
        for existing in all_documents:
            if existing.metadata.get("id") == document.metadata.get("id"):
                found = True
        if not found:
            all_documents.append(document)

    start = time.time()
    reranked_documents = rank_docs(all_documents, query_text)
    end = time.time()
    time_rerank = end - start

    response_text = ""
    for document in reranked_documents:
        response_text += f"\n{document.metadata.get('source')} \nTime {document.metadata.get('time')} \n"

    # print("Times")
    # print("-----------------")
    # print(f"Dense retrieval: {time_dense}")
    # print(f"Sparse retrieval: {time_sparse}")
    # print(f"Relevant dense: {time_relevant_dense}")
    # print(f"Relevant sparse: {time_relevant_sparse}")
    # print(f"Rerank: {time_rerank}")
    return response_text, reranked_documents