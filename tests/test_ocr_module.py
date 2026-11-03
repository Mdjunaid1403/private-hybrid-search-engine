from app.ocr import extract_text_from_image
from PIL import Image


image = Image.open(
    "multilingual_test.png"
)

text = extract_text_from_image(
    image,
    "eng+kan"
)

print("OCR result:")
print("-----------")
print(text)