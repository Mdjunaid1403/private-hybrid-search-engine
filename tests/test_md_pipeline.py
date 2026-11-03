from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding


markdown_content = """# Private Search Engine

A private search engine allows users to search their own documents.

## Search Types

The system supports keyword search, semantic search, hybrid search, and web search.

## Technologies

The backend uses Python and FastAPI.
The database uses PostgreSQL and pgvector.
The semantic search uses Sentence Transformers.
"""

file_bytes = markdown_content.encode("utf-8")

text = extract_text(
    file_bytes,
    "test.md"
)

print("Extracted text:")
print(text)

chunks = create_chunks(text)

print("\nNumber of chunks:")
print(len(chunks))

for i, chunk in enumerate(chunks):
    embedding = generate_embedding(chunk)

    print(
        f"Chunk {i + 1}: "
        f"Embedding shape = {embedding.shape}"
    )