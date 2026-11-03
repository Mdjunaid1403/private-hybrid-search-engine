from app.document_parser import extract_text


try:
    extract_text(
        b"This is a test.",
        "test.doc"
    )

except ValueError as error:
    print(error)