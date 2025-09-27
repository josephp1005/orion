from langchain_community.embeddings import ollama


def get_embedding_function():
    ollama_emb = ollama.OllamaEmbeddings(model='nomic-embed-text')

    return ollama_emb


if __name__ == "__main__":
    test_vectorizer = get_embedding_function()
    print(test_vectorizer)