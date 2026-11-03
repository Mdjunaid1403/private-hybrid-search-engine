from pathlib import Path

from app.document_parser import extract_html_text


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


print("\nExtracted text:")
print("----------------")

print(
    text[:5000]
)

print("\n----------------")

print("Character count:")
print(len(text))