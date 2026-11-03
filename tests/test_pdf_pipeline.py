from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding


import pymupdf


pdf_document = pymupdf.open()

page = pdf_document.new_page()

page.insert_text(
    (72, 72),
    "Python is a programming language. "
    "FastAPI is a Python web framework."
)

pdf_bytes = pdf_document.tobytes()

pdf_document.close()


text = extract_text(
    pdf_bytes,
    "test.pdf"
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