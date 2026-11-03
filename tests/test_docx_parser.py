from docx import Document

from app.document_parser import extract_text


document = Document()

document.add_paragraph(
    "This is a test DOCX document for the private search engine."
)

document.add_paragraph(
    "Python, FastAPI, and PostgreSQL are used in this project."
)

file_bytes = None

from io import BytesIO

file_stream = BytesIO()

document.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.docx"
)

print(text)