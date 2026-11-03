import pytesseract
from PIL import Image


image = Image.open("multilingual_test.png")

text = pytesseract.image_to_string(
    image,
    lang="eng+kan"
)

print("OCR result:")
print("-----------")
print(text)