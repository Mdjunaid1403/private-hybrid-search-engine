from app.document_parser import extract_text
from app.embeddings import (
    create_chunks,
    generate_embedding
)


csv_content = """Technology,Description
Python,Programming language
FastAPI,Python web framework
PostgreSQL,Relational database
"""

file_bytes = csv_content.encode("utf-8")


text = extract_text(
    file_bytes,
    "test.csv"
)

print("Extracted text:")
print(text)

print("\nCreating chunks...")

chunks = create_chunks(text)

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print("\nChunk:")
    print(chunk)

    embedding = generate_embedding(chunk)

    print("Embedding shape:", embedding.shape)