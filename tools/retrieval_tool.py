def retrieve_context(memory, query: str, k: int = 5):
    results = memory.search(query, limit=k)
    return {"type": "retrieval", "results": results}
