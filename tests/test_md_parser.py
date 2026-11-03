from app.document_parser import extract_text


markdown_content = """# Private Search Engine

This is a Markdown document.

## Features

- Keyword search
- Semantic search
- Hybrid search
- Web search

**PostgreSQL** is used as the database.

```python
print("Hello")
"""

file_bytes = markdown_content.encode("utf-8")

text = extract_text(
    file_bytes,
    "test.md"
)

print("Extracted Markdown:")
print ("--------------------")
print(text)