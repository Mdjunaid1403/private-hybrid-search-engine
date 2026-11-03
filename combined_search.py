from hybrid_search import hybrid_search
from app.search import search_web


def combined_search(query, user_id, private_limit=5, web_limit=5):
    private_results = hybrid_search(
        query,
        user_id,
        limit=private_limit
    )

    web_results = search_web(
        query,
        max_results=web_limit
    )

    return {
        "query": query,
        "private_results": private_results,
        "web_results": web_results
    }