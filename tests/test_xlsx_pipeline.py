from io import BytesIO

from openpyxl import Workbook

from app.document_parser import extract_text
from app.embeddings import (
    create_chunks,
    generate_embedding
)


workbook = Workbook()

worksheet = workbook.active

worksheet.title = "Technology"

worksheet.append([
    "Technology",
    "Description"
])

worksheet.append([
    "Python",
    "Programming language"
])

worksheet.append([
    "FastAPI",
    "Python web framework"
])

worksheet.append([
    "PostgreSQL",
    "Relational database"
])


file_stream = BytesIO()

workbook.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.xlsx"
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