from pathlib import Path

from app.document_parser import extract_html_text


html_file = Path(
    "html_ocr_test/test_image.html"
)

html_bytes = html_file.read_bytes()

base_dir = html_file.parent


text = extract_html_text(
    html_bytes,
    base_dir=base_dir
)


print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")