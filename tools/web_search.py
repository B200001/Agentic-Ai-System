from ddgs import DDGS

def web_search(query: str, max_results: int = 5):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body"),
                })
    except Exception:
        return {"type": "search", "query": query, "results": [], "error": "Search failed"}

    return {"type": "search", "query": query, "results": results}

