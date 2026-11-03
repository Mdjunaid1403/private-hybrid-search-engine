from io import BytesIO

from pptx import Presentation

from app.document_parser import extract_text
from app.embeddings import (
    create_chunks,
    generate_embedding
)


presentation = Presentation()

slide1 = presentation.slides.add_slide(
    presentation.slide_layouts[1]
)

slide1.shapes.title.text = "Python"

slide1.placeholders[1].text = (
    "Python is a programming language."
)

slide2 = presentation.slides.add_slide(
    presentation.slide_layouts[1]
)

slide2.shapes.title.text = "FastAPI"

slide2.placeholders[1].text = (
    "FastAPI is a Python web framework."
)


file_stream = BytesIO()

presentation.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.pptx"
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