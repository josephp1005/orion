import json
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from aggregate_documents import LLM_MODEL
from supabase_client import get_docs_structure
from dotenv import load_dotenv
import os

load_dotenv()

def get_curation_prompt():
    return PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert technical writer and database administrator. Your task is to keep documentation up-to-date by generating SQL queries.
You will be given the current documentation structure and a set of new information chunks.
Based on this, generate a list of Supabase SQL queries to perform `INSERT`, `UPDATE`, or `DELETE` operations on the documentation.

Respond with a single JSON object containing one key: "queries". The value should be a list of SQL query strings.

It is vital that you produce valid JSON.

Example response:
{{
  "queries": [
    "UPDATE page_blocks SET content = 'New updated content.' WHERE id = 'some-uuid';",
    "INSERT INTO pages (id, collection_id, slug, title, position) VALUES ('new-uuid', 'existing-collection-uuid', 'new-page', 'New Page Title', 3);"
  ]
}}

Here is the current documentation structure:
{docs_structure}
<|eot_id|><|start_header_id|>user<|end_header_id|>
Here are the new information chunks to analyze:
{new_chunks}

Here are the table schemas:
- `collections` (id, slug, label, position)
- `pages` (id, collection_id, slug, title, position)
- `page_blocks` (id, page_id, kind, content, position, meta)

ONLY modify the tables which are named "collections", "pages", or "page_blocks". There are NO other table names.

- `kind` can be 'heading', 'markdown', or 'code'. Use the Markdown markup language for 'markdown' kind.
- Ensure all SQL is valid for PostgreSQL.
- Escape single quotes in content by doubling them (e.g., 'it''s').
- If the new information is irrelevant, conversational, or not useful, return an empty list of queries.

Please provide your response as a single JSON object with the "queries" key. \n
Only output a single valid JSON object. Do not include any explanation or extra text.

return valid json or you will be terminated.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
""",
        input_variables=["docs_structure", "new_chunks"],
    )

async def get_documentation_suggestions(new_chunks: list) -> list:
    """
    Uses an LLM to get a list of SQL queries to update documentation.
    """
    # llm = ChatOllama(model=LLM_MODEL, temperature=0.4)

    # inference_server_url = "https://api.openai.com/v1"
    
    # llm = ChatOpenAI(
    #     model="gpt-5",
    #     openai_api_key=os.getenv("OPENAI_API_KEY"),
    #     openai_api_base=inference_server_url,
    #     temperature=1
    # )

    inference_server_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    llm = ChatOpenAI(
        model="gemini-2.5-flash",
        openai_api_key=os.getenv("GEMINI_KEY"),
        openai_api_base=inference_server_url,
        temperature=0
    )
    
    prompt = get_curation_prompt()
    
    docs_structure = get_docs_structure()
    if not docs_structure:
        return []

    # Format chunks for the prompt
    formatted_chunks = "\n---\n".join([f"Source: {chunk.metadata.get('source')}\nContent: {chunk.page_content}" for chunk in new_chunks])

    chain = prompt | llm
    response = await chain.ainvoke({
        "docs_structure": docs_structure,
        "new_chunks": formatted_chunks
    })

    try:
        # Clean up the response and parse JSON
        response_text = response.content.replace("```json", "").replace("```", "").strip()
        suggestions_json = json.loads(response_text)
        return suggestions_json.get("queries", [])
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        print(f"LLM Response:\n{response.content}")
        return []