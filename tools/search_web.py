from langchain.tools import tool
from langsmith import traceable
from langchain_google_community import GoogleSearchAPIWrapper
import json
from dotenv import load_dotenv
load_dotenv()
import os

try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    print("✅ Setup and authentication complete.")
except Exception as e:
    print(
        f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' and 'GOOGLE_CSE_ID' in your .env file"
    )

_search_wrapper = GoogleSearchAPIWrapper(
    google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID
)

@tool
@traceable(name="web_search")
def web_search(query: str, k: int = 1) -> str:
    '''
    Search the web for companies using the given tech stack and return structured JSON.
    
    Args:
        query: The query to search for
        k: The number of results to return
    Returns:
        A JSON object containing the results of the search
    '''
    query = (query or "").strip()
    try:
        results = _search_wrapper.results(query, k)
    except Exception as e:
        return json.dumps({"query": query, "status": "error", "message": str(e), "results": []})

    if not results:
        return json.dumps({"query": query, "status": "no_results", "results": []})

    print(results)
    normalized = [
        {"title": r.get("title", ""), "link": r.get("link", ""), "snippet": r.get("snippet", "")}
        for r in results[:k]
    ]
    print(normalized)
    return json.dumps({"query": query, "status": "ok", "results": normalized})