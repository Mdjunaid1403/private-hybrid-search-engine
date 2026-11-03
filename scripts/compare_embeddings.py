from sentence_transformers import SentenceTransformer
from app.db import get_connection


model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_text = "Python is a programming language used for software development. It"

new_embedding = model.encode(chunk_text)


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT embedding
    FROM document_chunks
    WHERE id = 1;
""")

stored_embedding = cur.fetchone()[0]

stored_embedding = stored_embedding.strip("[]")
stored_embedding = [float(value) for value in stored_embedding.split(",")]

cur.close()
conn.close()


print("New embedding dimensions:", len(new_embedding))
print("Stored embedding dimensions:", len(stored_embedding))

print("First value of new embedding:", new_embedding[0])
print("First value of stored embedding:", stored_embedding[0])