
import logging

from ddgs import DDGS
from ddgs.exceptions import DDGSException

logger = logging.getLogger(__name__)


def search_web(query, max_results=5):
    try:
        with DDGS(timeout=10) as ddgs:
            results = ddgs.text(
                query,
                max_results=max_results
            )

            logger.info(
                "Web search query=%r returned %d results",
                query,
                len(results)
            )

            return results

    except DDGSException:
        logger.exception(
            "Web search failed for query=%r",
            query
        )
        return []
