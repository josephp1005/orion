from aggregate_documents import LLM_MODEL
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from get_relevant_docs import get_docs
import argparse
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


"""
Takes in a list of documents and a string question.

Outputs which of those documents are relevant to the question and which are not, both as lists.
"""
def response(documents: list[Document], question: str):
    llm = ChatOllama(model=LLM_MODEL, temperature=0)    
    # inference_server_url = "https://api.openai.com/v1"
    
    # llm = ChatOpenAI(
    #     model="gpt-5",
    #     openai_api_key=os.getenv("OPENAI_API_KEY"),
    #     openai_api_base=inference_server_url,
    #     temperature=0
    # )

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You will be given a user query along 
        with a list of potentially helpful documents in answering that query. Answer the query. 
        Do not provide a preamble. Rather than saying info is from "Documents", mention their specific source. \n
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
        doc_time = document.metadata.get("time")
        document_text += f"\n Source: {doc_source} Time: {doc_time} \n Content: {doc_content} \n"

    output = generator.invoke({"question": question, "documents": document_text})

    return output.content


def rag_pipeline(query: str):
    formatted_doc_list, docs = get_docs(query)
    output = response(docs, query)

    return formatted_doc_list, output, docs

def sort_doc_by_time(doc_list):
    doc_list.sort(
        key=lambda doc: datetime.strptime(doc.metadata["time"], "%Y-%m-%d %H:%M:%S")
    )

def format_sorted_docs(doc_list):
    response = []
    for document in doc_list:
        response.append({"source": document.metadata["source"], "time": document.metadata["time"], "content": document.page_content, "type": document.metadata["type"]})

    return response

def docs_and_response(query: str):
    formatted_doc_list, output, docs = rag_pipeline(query)
    sort_doc_by_time(docs)
    sorted_docs_response = format_sorted_docs(docs)

    return {"docs": sorted_docs_response, "response": output}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    formatted_doc_list, output, docs = rag_pipeline(query_text)
    sort_doc_by_time(docs)

    sorted_docs_response = format_sorted_docs(docs)

    print(sorted_docs_response)
    print(output)   


if __name__ == "__main__":
    main()