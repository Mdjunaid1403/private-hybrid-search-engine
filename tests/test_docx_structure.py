import zipfile
import re


file_path = r"C:\Users\Junaid\Projects\private-search-engine\SIR DRAFT LIST (118).docx"


with zipfile.ZipFile(file_path) as docx:
    document_xml = docx.read(
        "word/document.xml"
    ).decode("utf-8")

    text_matches = re.findall(
        r"<w:t[^>]*>(.*?)</w:t>",
        document_xml
    )

    image_files = [
        name
        for name in docx.namelist()
        if name.startswith("word/media/")
    ]


print("Text elements found:", len(text_matches))

print("\nFirst text elements:")

for text in text_matches[:20]:
    print(text)

print("\nImages found:", len(image_files))

for image in image_files:
    print(image)