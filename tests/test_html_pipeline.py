from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding


html_content = """
<html>

<body>

<h1>Private Search Engine</h1>

<p>
A private search engine allows users to search
their own documents.
</p>

<h2>Semantic Search</h2>

<p>
Semantic search uses embeddings to understand
the meaning of a query.
</p>

<h2>Hybrid Search</h2>

<p>
Hybrid search combines keyword search and
semantic search.
</p>

<h2>Database</h2>

<p>
PostgreSQL and pgvector are used to store
documents and embeddings.
</p>

</body>

</html>
"""

file_bytes = html_content.encode("utf-8")

text = extract_text(
    file_bytes,
    "test.html"
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