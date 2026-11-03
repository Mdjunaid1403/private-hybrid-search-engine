from app.document_parser import extract_html_text


html = """
<!DOCTYPE html>

<html>
<head>
    <title>External Image OCR Test</title>
</head>

<body>

<h1>External Image OCR Test</h1>

<p>
This text comes directly from HTML.
</p>

<img
    src="https://dummyimage.com/800x250/ffffff/000000.png&text=Private+Search+Engine+OCR+Test"
    alt="External OCR test image"
>

</body>
</html>
"""


text = extract_html_text(
    html.encode("utf-8")
)

print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")