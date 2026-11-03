from app.document_parser import extract_text


csv_content = """Name,Age,City
Junaid,21,Mysore
Ahmed,22,Bangalore
"""

file_bytes = csv_content.encode("utf-8")


text = extract_text(
    file_bytes,
    "test.csv"
)

print(text)