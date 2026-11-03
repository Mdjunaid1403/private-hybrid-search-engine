from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding


filename = "test_scanned.pdf"

with open(filename, "rb") as file:
    file_bytes = file.read()


print("Extracting PDF text with OCR...")

text = extract_text(
    file_bytes,
    filename
)

print("Character count:")
print(len(text))


print("\nCreating chunks...")

chunks = create_chunks(text)

print("Number of chunks:")
print(len(chunks))


print("\nTesting embeddings...")

test_count = min(5, len(chunks))

for i in range(test_count):

    embedding = generate_embedding(
        chunks[i]
    )

    print(
        f"Chunk {i + 1}: "
        f"Embedding shape = {embedding.shape}"
    )