
from app.local_search import search_documents
from app.indexer import build_index
from app.database import get_documents_for_search
from semantic_search import semantic_search


def hybrid_search(query, user_id, limit=5):

    # Retrieve documents belonging to the current user.
    database_documents = get_documents_for_search(user_id)

    # Build keyword index.
    index = build_index(database_documents)

    # Perform keyword search.
    keyword_results = search_documents(index, query)

    # Map filenames to database IDs.
    document_map = {
        document["filename"]: document["id"]
        for document in database_documents
    }

    # Store keyword relevance scores.
    keyword_scores = {}

    for filename, score in keyword_results:
        keyword_scores[filename] = score

    # Perform semantic search.
    semantic_results = semantic_search(query, user_id, limit)

    semantic_scores = {}

    for result in semantic_results:
        filename = result[2]
        distance = result[4]

        similarity = max(0, 1 - distance)

        semantic_scores[filename] = max(
            semantic_scores.get(filename, 0),
            similarity
        )

    # Combine all matching documents.
    all_filenames = (
        set(keyword_scores)
        | set(semantic_scores)
    )

    hybrid_results = []

    for filename in all_filenames:

        keyword_score = keyword_scores.get(filename, 0)
        semantic_score = semantic_scores.get(filename, 0)

        # Give keyword matches priority.
        if keyword_score > 0 and semantic_score == 0:
            hybrid_score = keyword_score

        elif semantic_score > 0 and keyword_score == 0:
            hybrid_score = semantic_score * 0.6

        else:
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

    hybrid_results.sort(
        key=lambda result: result["hybrid_score"],
        reverse=True
    )

    return hybrid_results[:limit]