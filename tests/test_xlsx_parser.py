from io import BytesIO

from openpyxl import Workbook

from app.document_parser import extract_text


workbook = Workbook()

worksheet = workbook.active
worksheet.title = "Students"

worksheet.append([
    "Name",
    "Age",
    "City"
])

worksheet.append([
    "Junaid",
    21,
    "Mysore"
])

worksheet.append([
    "Ahmed",
    22,
    "Bangalore"
])


file_stream = BytesIO()

workbook.save(file_stream)

file_bytes = file_stream.getvalue()

file_stream.close()


text = extract_text(
    file_bytes,
    "test.xlsx"
)

print(text)