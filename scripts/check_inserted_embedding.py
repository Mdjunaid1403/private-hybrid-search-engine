from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT id, document_id, chunk_text, embedding
    FROM document_chunks
    WHERE id = 1;
""")

result = cur.fetchone()

print("Chunk ID:", result[0])
print("Document ID:", result[1])
print("Chunk text:", result[2])
print("Embedding:", result[3])

cur.close()
conn.close()