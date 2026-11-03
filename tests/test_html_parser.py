from app.document_parser import extract_text


html_content = """
<!DOCTYPE html>

<html>

<head>
    <title>Private Search Engine</title>

    <style>
        body {
            background: white;
        }
    </style>

    <script>
        console.log("This should not appear");
    </script>
</head>

<body>

    <h1>Private Search Engine</h1>

    <p>
        This is a private search engine project.
    </p>

    <h2>Features</h2>

    <ul>
        <li>Keyword Search</li>
        <li>Semantic Search</li>
        <li>Hybrid Search</li>
    </ul>

    <p>
        PostgreSQL stores the documents.
    </p>

</body>

</html>
"""

file_bytes = html_content.encode("utf-8")

text = extract_text(
    file_bytes,
    "test.html"
)

print("Extracted HTML text:")
print("--------------------")
print(text)