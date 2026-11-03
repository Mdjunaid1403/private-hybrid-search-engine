from app.embeddings import generate_embedding
from app.db import get_connection


query = "How do computers learn from data?"

query_embedding = generate_embedding(query)


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT vector_dims(%s::vector);
""", (query_embedding.tolist(),))

dimension = cur.fetchone()[0]

print("Query vector dimension in PostgreSQL:", dimension)

cur.close()
conn.close()