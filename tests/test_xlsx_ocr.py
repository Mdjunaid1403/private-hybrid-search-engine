from pathlib import Path

from app.document_parser import extract_xlsx_text


xlsx_path = Path(
    "test_ocr.xlsx"
)


with open(
    xlsx_path,
    "rb"
) as file:

    file_bytes = file.read()


print("Extracting XLSX text with OCR...")

text = extract_xlsx_text(
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