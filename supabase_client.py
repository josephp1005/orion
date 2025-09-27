import os
from supabase import create_client, Client
from dotenv import load_dotenv
import psycopg2
from typing import Iterable, Union


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


def execute_documentation_changes(queries: Iterable[Union[str, dict]]):
    results = []
    for item in queries:
        sql = item
        try:
            supabase.rpc("execute_sql", {"query": sql}).execute()
            results.append({"query": sql, "status": "success"})
        except Exception as e:
            results.append({"query": sql, "status": "error", "details": str(e)})
    return results