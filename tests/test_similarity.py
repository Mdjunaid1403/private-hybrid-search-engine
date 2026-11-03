from app.embeddings import generate_embedding
from app.db import get_connection


query = "How do computers learn from data?"

query_embedding = generate_embedding(query)


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT id, chunk_text, embedding <=> %s::vector AS distance
    FROM document_chunks
    WHERE id = 2;
""", (query_embedding.tolist(),))

result = cur.fetchone()

print("Chunk ID:", result[0])
print("Chunk text:", result[1])
print("Cosine distance:", result[2])

cur.close()
conn.close()