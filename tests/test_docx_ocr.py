from app.document_parser import extract_text


filename = "SIR DRAFT LIST (118).docx"

with open(filename, "rb") as file:
    file_bytes = file.read()


text = extract_text(
    file_bytes,
    filename
)

print("Extracted text:")
print("----------------")
print(text)

print("\nCharacter count:")
print(len(text))