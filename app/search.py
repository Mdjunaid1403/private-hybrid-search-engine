
import logging
import time

from ddgs import DDGS
from ddgs.exceptions import DDGSException

logger = logging.getLogger(__name__)


def search_web(query, max_results=5):
    for attempt in range(2):
        try:
            with DDGS(timeout=20) as ddgs:
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
                "Web search failed on attempt %d for query=%r",
                attempt + 1,
                query
            )

            if attempt == 0:
                time.sleep(1)

    return []
