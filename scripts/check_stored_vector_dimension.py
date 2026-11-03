from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT vector_dims(embedding)
    FROM document_chunks
    WHERE id = 1;
""")

dimension = cur.fetchone()[0]

print("Stored vector dimension:", dimension)

cur.close()
conn.close()
