import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_docs_structure():
    """Fetches all collections, pages, and their blocks from Supabase and formats them into a structured string."""
    try:
        response = supabase.from_("collections").select("*, pages(*, page_blocks(*))").execute()
        data = response.data
        
        if not data:
            return "No documentation found."

        output = []
        for collection in data:
            collection_info = {k: v for k, v in collection.items() if k != 'pages'}
            output.append(f"Collection: {collection_info}")
            
            if collection.get('pages'):
                # Sort pages by position
                sorted_pages = sorted(collection['pages'], key=lambda p: p.get('position', 0))
                for page in sorted_pages:
                    page_info = {k: v for k, v in page.items() if k != 'page_blocks'}
                    output.append(f"  Page: {page_info}")
                    
                    if page.get('page_blocks'):
                        # Sort blocks by position
                        sorted_blocks = sorted(page['page_blocks'], key=lambda b: b.get('position', 0))
                        for block in sorted_blocks:
                            output.append(f"    Block: {block}")
            output.append("-" * 20)
        
        return "\n".join(output)
        
    except Exception as e:
        print(f"Error fetching docs structure: {e}")
        return None

def execute_documentation_changes(queries: list[str]):
    """
    Executes a list of SQL queries against the Supabase database.

    Args:
        queries: A list of SQL query strings to execute.

    Returns:
        A list of dictionaries, each containing the query and its result ('success' or 'error').
    """
    results = []
    for query in queries:
        try:
            supabase.sql(query).execute()
            results.append({"query": query, "status": "success"})
            print(f"Successfully executed: {query}")
        except Exception as e:
            error_message = f"Error executing query: {query}\n{e}"
            print(error_message)
            results.append({"query": query, "status": "error", "details": str(e)})
    return results