from pathlib import Path

from app.document_parser import extract_html_text
from app.embeddings import create_chunks, generate_embedding


html_path = Path(
    "test_ocr.html"
)


with open(
    html_path,
    "rb"
) as file:

    file_bytes = file.read()


print("Extracting HTML text with OCR...")

text = extract_html_text(
    file_bytes
)

print("Character count:")
print(len(text))


print("\nCreating chunks...")

chunks = create_chunks(
    text
)

print("Number of chunks:")
print(len(chunks))


print("\nTesting embeddings...")

for index, chunk in enumerate(
    chunks[:5],
    start=1
):

    embedding = generate_embedding(
        chunk
    )

    print(
        f"Chunk {index}: "
        f"Embedding shape = "
        f"{embedding.shape}"
    )