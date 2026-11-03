from ddgs import DDGS
from ddgs.exceptions import DDGSException

def search_web(query, max_results=5):
    try:
        with DDGS() as ddgs:
            return ddgs.text(query, max_results=max_results)
    except DDGSException:
        return []
