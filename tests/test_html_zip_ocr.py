from pathlib import Path

from app.document_parser import extract_text


zip_file = Path(
    "html_ocr_test.zip"
)

zip_bytes = zip_file.read_bytes()


text = extract_text(
    zip_bytes,
    zip_file.name
)


print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")