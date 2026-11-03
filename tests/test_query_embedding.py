from app.embeddings import generate_embedding


query = "How do computers learn from data?"

query_embedding = generate_embedding(query)

print("Query:", query)
print("Embedding shape:", query_embedding.shape)
print("First value:", query_embedding[0])
print("Number of values:", len(query_embedding))