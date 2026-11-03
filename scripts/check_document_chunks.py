from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT id, document_id, chunk_text, vector_dims(embedding)
    FROM document_chunks
    ORDER BY id;
""")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()