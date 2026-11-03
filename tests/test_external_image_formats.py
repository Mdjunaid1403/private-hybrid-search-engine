from app.document_parser import extract_html_text


with open(
    "test_external_image_formats.html",
    "rb"
) as file:

    html_bytes = file.read()


text = extract_html_text(
    html_bytes
)

print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")