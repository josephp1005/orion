from aggregate_documents import LLM_MODEL
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from get_relevant_docs import get_docs
import argparse


"""
Takes in a list of documents and a string question.

Outputs which of those documents are relevant to the question and which are not, both as lists.
"""
def response(documents: list[Document], question: str):
    llm = ChatOllama(model=LLM_MODEL, temperature=0)

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You will be given a user query along 
        with a list of potentially helpful documents in answering that query.
        Answer the query, and provide helpful guidance for further learning. Do not provide a preamble. \n
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here are the retrieved documents: \n\n {documents} \n\n
        Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "documents"],
    )

    generator = prompt | llm

    document_text = ""
    for document in documents:
        doc_content = document.page_content
        doc_source = document.metadata.get("source")
        doc_page = document.metadata.get("page")
        document_text += f"\n Source: {doc_source} Page: {doc_page} \n Content: {doc_content} \n"

    output = generator.invoke({"question": question, "documents": document_text})

    return output.content


def rag_pipeline(query: str):
    formatted_doc_list, docs = get_docs(query)
    output = response(docs, query)

    return formatted_doc_list, output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    formatted_doc_list, output = rag_pipeline(query_text)

    print(output)


if __name__ == "__main__":
    main()