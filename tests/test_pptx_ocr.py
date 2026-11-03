from pathlib import Path

from app.document_parser import extract_pptx_text


pptx_path = Path(
    "test_ocr.pptx"
)


with open(
    pptx_path,
    "rb"
) as file:

    file_bytes = file.read()


print("Extracting PPTX text with OCR...")

text = extract_pptx_text(
    file_bytes
)


print("\nExtracted text:")
print("----------------")

print(
    text[:5000]
)

print("\n----------------")

print("Character count:")
print(len(text))