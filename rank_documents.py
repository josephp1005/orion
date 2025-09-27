from sentence_transformers import CrossEncoder
from langchain.schema import Document
from aggregate_documents import CROSS_ENCODER_MODEL

"""
Reranking documents with a cross encoder based on relevance to query.
"""
def rank_docs(documents: list[Document], query: str):
    if len(documents) == 0:
        return documents
    model = CrossEncoder(CROSS_ENCODER_MODEL)
    ranks = model.rank(query, [document.page_content for document in documents])

    reordered = []
    for rank in ranks:
        reordered.append(documents[rank['corpus_id']])

    return reordered


if __name__ == "__main__":
    pass
