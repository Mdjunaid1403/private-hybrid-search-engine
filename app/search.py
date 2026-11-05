import logging
import math
import re
import time
from collections import Counter

from ddgs import DDGS
from ddgs.exceptions import DDGSException

from importlib.metadata import version

logger = logging.getLogger(__name__)

STOP_WORDS = {
    "find", "show", "search", "which", "what", "where",
    "the", "a", "an", "and", "or", "to", "of", "that",
    "for", "is", "are", "was", "were", "be", "been",
    "in", "on", "at", "by", "with", "how", "do", "does",
    "other", "problem", "problems", "finding",
    "element", "elements"
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def cosine_similarity(query, document):
    query_words = tokenize(query)
    document_words = tokenize(document)

    if not query_words or not document_words:
        return 0.0

    # documents = [query_words, document_words]

    document_frequency = Counter(
        word
        for word in set(query_words)
        for _ in [0]
    )

    for word in set(document_words):
        document_frequency[word] += 1

    def make_vector(words):
        counts = Counter(words)
        vector = {}

        for word, count in counts.items():
            idf = math.log(
                1 + 2 / (1 + document_frequency[word])
            )
            vector[word] = (1 + math.log(count)) * idf

        return vector

    query_vector = make_vector(query_words)
    document_vector = make_vector(document_words)

    dot_product = sum(
        value * document_vector.get(word, 0)
        for word, value in query_vector.items()
    )

    query_norm = math.sqrt(
        sum(value ** 2 for value in query_vector.values())
    )
    document_norm = math.sqrt(
        sum(value ** 2 for value in document_vector.values())
    )

    if not query_norm or not document_norm:
        return 0.0

    return dot_product / (query_norm * document_norm)


def filter_relevant_results(query, results):
    relevant_results = []
    seen_urls = set()

    query_words = set(tokenize(query))
    minimum_matches = min(2, len(query_words))

    for result in results:
        title = (result.get("title") or "").strip()
        body = (result.get("body") or "").strip()
        url = (result.get("href") or "").strip()

        # Reject incomplete results
        if not title or not body or not url:
            continue

        # Reject suspiciously long titles
        if len(title) > 180:
            continue

        # Reject concatenated titles
        concatenated_parts = re.findall(r"[a-z][A-Z]", title)

        if len(concatenated_parts) >= 2:
            continue

        # Remove duplicate URLs
        normalized_url = url.rstrip("/").lower()

        if normalized_url in seen_urls:
            continue

        # Calculate meaningful keyword matches
        result_words = set(tokenize(f"{title} {body}"))
        matched_words = query_words.intersection(result_words)

        if len(matched_words) < minimum_matches:
            continue

        # Calculate similarity
        score = cosine_similarity(
            query,
            f"{title} {body}"
        )

        if score < 0.10:
            continue

        seen_urls.add(normalized_url)

        result["_relevance_score"] = score
        relevant_results.append(result)

    relevant_results.sort(
        key=lambda item: item["_relevance_score"],
        reverse=True
    )

    for result in relevant_results:
        result.pop("_relevance_score", None)

    return relevant_results


def search_web(query, max_results=5):
    fallback_queries = [
        query,
        re.sub(r"[^\w\s]", " ", query),
        " ".join(tokenize(query))
    ]

    fallback_queries = list(dict.fromkeys(
        q.strip() for q in fallback_queries if q.strip()
    ))

    all_results = []

    logger.info(
        "DIAGNOSTIC: Installed DDGS version: %s",
        version("ddgs")
    )

    for search_query in fallback_queries:
        for attempt in range(2):
            try:
                with DDGS(timeout=20) as ddgs:
                    results = ddgs.text(
                        search_query,
                        max_results=max_results,
                        backend="yahoo"
                    )

                logger.info(
                    "DIAGNOSTIC: Query=%r | Raw result count=%d | Titles=%r",
                    search_query,
                    len(results),
                    [r.get("title", "") for r in results]
                )

                all_results.extend(results)

                if results:
                    break

            except DDGSException as exc:
                logger.warning(
                    "Web search attempt %d failed for query=%r: %s",
                    attempt + 1,
                    search_query,
                    exc
                )

                if attempt == 0:
                    time.sleep(1)

    relevant_results = filter_relevant_results(
        query,
        all_results
    )

    logger.info(
        "DIAGNOSTIC: Original query=%r | Total raw results=%d | Filtered results=%d | Final titles=%r",
        query,
        len(all_results),
        len(relevant_results),
        [r.get("title", "") for r in relevant_results]
    )

    logger.info(
        "Original query=%r, collected=%d, relevant=%d",
        query,
        len(all_results),
        len(relevant_results)
    )

    return relevant_results[:max_results]
