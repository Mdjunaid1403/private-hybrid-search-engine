from app.embeddings import generate_embedding
from app.db import get_connection


def semantic_search(query, user_id, limit=5):
    query_embedding = generate_embedding(query)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM (
        SELECT
            document_chunks.id,
            document_chunks.document_id,
            documents.filename,
            document_chunks.chunk_text,
            document_chunks.embedding <=> %s::vector AS distance
        FROM document_chunks
        JOIN documents
            ON document_chunks.document_id = documents.id
        WHERE documents.user_id = %s
    ) AS semantic_results
    WHERE distance <= 0.50
    ORDER BY distance
    LIMIT %s;
""", (query_embedding.tolist(), user_id, limit))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results