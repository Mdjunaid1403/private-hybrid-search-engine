from app.document_parser import extract_text


filename = "test_scanned.pdf"

with open(filename, "rb") as file:
    file_bytes = file.read()


print("Extracting PDF text...")

text = extract_text(
    file_bytes,
    filename
)

print("\nExtracted text:")
print("----------------")
print(text)

print("\nCharacter count:")
print(len(text))