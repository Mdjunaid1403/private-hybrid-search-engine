import pymupdf

from app.document_parser import extract_text


pdf_document = pymupdf.open()

page1 = pdf_document.new_page()

page1.insert_text(
    (72, 72),
    "This is page one of the test PDF."
)

page2 = pdf_document.new_page()

page2.insert_text(
    (72, 72),
    "This is page two of the test PDF."
)

page3 = pdf_document.new_page()

page3.insert_text(
    (72, 72),
    "This is page three of the test PDF."
)

pdf_bytes = pdf_document.tobytes()

pdf_document.close()


text = extract_text(
    pdf_bytes,
    "test.pdf"
)

print(text)