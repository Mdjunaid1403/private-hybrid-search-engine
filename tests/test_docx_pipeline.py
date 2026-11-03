from io import BytesIO

from docx import Document

from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding


document = Document()

document.add_paragraph(
    "Python is a programming language. "
    "FastAPI is a Python web framework."
)

document.add_paragraph(
    "PostgreSQL is a relational database system "
    "used by the private search engine."
)


file_stream = BytesIO()

document.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.docx"
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