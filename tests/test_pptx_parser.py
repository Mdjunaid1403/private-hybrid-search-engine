from io import BytesIO

from pptx import Presentation

from app.document_parser import extract_text


presentation = Presentation()

slide = presentation.slides.add_slide(
    presentation.slide_layouts[1]
)

slide.shapes.title.text = "Private Search Engine"

slide.placeholders[1].text = (
    "This is a test PowerPoint presentation. "
    "Python, FastAPI, and PostgreSQL are used "
    "in this project."
)

file_stream = BytesIO()

presentation.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.pptx"
)

print(text)