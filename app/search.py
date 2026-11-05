
import logging
import re
import time

from ddgs import DDGS
from ddgs.exceptions import DDGSException

logger = logging.getLogger(__name__)


def search_web(query, max_results=5):
    # Prepare fallback queries
    fallback_queries = [
        query,
        re.sub(
            r"\b(find|show|search|which|problems|involving|about|other|for)\b",
            "",
            query,
            flags=re.IGNORECASE
        ),
        f"{query} programming algorithm LeetCode GeeksforGeeks"
    ]

    # Remove duplicate and empty queries
    fallback_queries = list(dict.fromkeys(
        q.strip() for q in fallback_queries if q.strip()
    ))

    for search_query in fallback_queries:
        for attempt in range(2):
            try:
                with DDGS(timeout=20) as ddgs:
                    results = ddgs.text(
                        search_query,
                        max_results=max_results,
                        backend="bing, google, brave, mojeek, yahoo"
                    )

                valid_results = [
                    result for result in results
                    if result.get("title", "").strip()
                    and result.get("href", "").strip()
                    and result.get("body", "").strip()
                ]

                if valid_results:
                    logger.info(
                        "Web search succeeded for query=%r "
                        "(original=%r), results=%d",
                        search_query,
                        query,
                        len(valid_results)
                    )
                    return valid_results

            except DDGSException as exc:
                logger.warning(
                    "Web search attempt %d failed for query=%r: %s",
                    attempt + 1,
                    search_query,
                    exc
                )

                if attempt == 0:
                    time.sleep(1)

    logger.warning("No web results found for original query=%r", query)
    return []
