# from app.documents import load_documents
from app.local_search import search_documents
from app.indexer import build_index
from app.database import get_documents_for_search
from semantic_search import semantic_search


def hybrid_search(query, user_id, limit=5):

    # Documents used for keyword search
    # Get documents from PostgreSQL
    database_documents = get_documents_for_search(user_id)

    index = build_index(database_documents)

    keyword_results = search_documents(index, query)

    # Documents from PostgreSQL
    # These contain the actual database IDs.
    # database_documents = get_documents_for_search()

    document_map = {
        document["filename"]: document["id"]
        for document in database_documents
    }

    # ---------------------------------
    # Semantic scores
    # ---------------------------------

    semantic_results = semantic_search(query, user_id, limit)

    semantic_scores = {}

    for result in semantic_results:
        filename = result[2]
        distance = result[4]

        similarity = max(0, 1 - distance)

        if filename not in semantic_scores:
            semantic_scores[filename] = similarity

        else:
            semantic_scores[filename] = max(semantic_scores[filename], similarity)

    # ---------------------------------
    # Keyword scores
    # ---------------------------------

    max_keyword_score = max(
        (score for _, score in keyword_results),
        default=0
    )

    keyword_scores = {}

    for filename, score in keyword_results:
        if max_keyword_score > 0:
            keyword_scores[filename] = (
                score / max_keyword_score
            )
        else:
            keyword_scores[filename] = 0

    # ---------------------------------
    # Combine results
    # ---------------------------------

    all_filenames = (
        set(keyword_scores)
        | set(semantic_scores)
    )

    hybrid_results = []

    for filename in all_filenames:
        keyword_score = keyword_scores.get(
            filename,
            0
        )

        semantic_score = semantic_scores.get(
            filename,
            0
        )

        hybrid_score = (
            keyword_score * 0.4
            + semantic_score * 0.6
        )

        if hybrid_score > 0:

            hybrid_results.append({

                "document_id": document_map.get(filename),

                "filename": filename,

                "keyword_score": keyword_score,

                "semantic_score": semantic_score,

                "hybrid_score": hybrid_score

            })

    # ---------------------------------
    # Sort by hybrid score
    # ---------------------------------

    hybrid_results.sort(
        key=lambda result:
            result["hybrid_score"],
        reverse=True
    )

    return hybrid_results[:limit]