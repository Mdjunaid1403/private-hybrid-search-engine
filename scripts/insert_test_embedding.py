from sentence_transformers import SentenceTransformer
from app.db import get_connection


model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_text = "Python is a programming language used for software development. It"

embedding = model.encode(chunk_text)


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    INSERT INTO document_chunks
        (document_id, chunk_text, embedding)
    VALUES
        (%s, %s, %s)
    RETURNING id;
""", (3, chunk_text, embedding.tolist()))

chunk_id = cur.fetchone()[0]

conn.commit()

print("Embedding inserted successfully")
print("Chunk ID:", chunk_id)

cur.close()
conn.close()