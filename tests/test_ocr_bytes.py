from app.ocr import extract_text_from_image_bytes


with open(
    "multilingual_test.png",
    "rb"
) as file:
    image_bytes = file.read()


text = extract_text_from_image_bytes(
    image_bytes,
    "eng+kan"
)

print("OCR result:")
print("-----------")
print(text)