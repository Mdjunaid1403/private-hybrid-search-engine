from app.db import get_connection


def store_chunk(document_id, chunk_text, embedding):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO document_chunks
            (document_id, chunk_text, embedding)
        VALUES
            (%s, %s, %s);
    """, (document_id, chunk_text, embedding.tolist()))

    conn.commit()

    cur.close()
    conn.close()