import io
import os
import pymupdf

import csv
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook
from bs4 import BeautifulSoup

from app.ocr import extract_text_from_image_bytes
import urllib.request

import tempfile
import zipfile
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".csv",
    ".md",
    ".html",
    ".zip"
}


def extract_text(file_bytes, filename):
    extension = os.path.splitext(filename)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    if extension == ".txt":
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError(
                "The uploaded .txt file must be valid UTF-8 text."
            )

    if extension == ".pdf":
        return extract_pdf_text(file_bytes)

    if extension == ".docx":
        return extract_docx_text(file_bytes)

    if extension == ".pptx":
        return extract_pptx_text(file_bytes)

    if extension == ".xlsx":
        return extract_xlsx_text(file_bytes)

    if extension == ".csv":
        return extract_csv_text(file_bytes)

    if extension == ".md":
        return extract_markdown_text(file_bytes)

    if extension == ".html":
        return extract_html_text(file_bytes)

    if extension == ".zip":
        return extract_html_zip_text(file_bytes)

    raise ValueError(
        f"Text extraction for {extension} is not implemented yet."
    )


def extract_pdf_text(file_bytes):
    pdf_document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []

    for page in pdf_document:

        page_text = page.get_text().strip()

        if page_text:
            pages.append(page_text)
            continue

        # No machine-readable text found.
        # Render the page as an image for OCR.
        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        image_bytes = pixmap.tobytes(
            "png"
        )

        ocr_text = extract_text_from_image_bytes(
            image_bytes
        )

        if ocr_text:
            pages.append(ocr_text)

    pdf_document.close()

    return "\n".join(pages)


def extract_docx_text(file_bytes):
    document = Document(
        io.BytesIO(file_bytes)
    )

    text_parts = []

    # Extract normal paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text_parts.append(
                paragraph.text
            )

    # Extract tables
    for table in document.tables:
        for row in table.rows:
            row_text = []

            for cell in row.cells:
                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                text_parts.append(" | ".join(row_text))

    # Extract and OCR embedded images
    ocr_parts = []

    for relationship in document.part.rels.values():

        if "image" not in relationship.reltype:
            continue

        image_part = relationship.target_part

        image_bytes = image_part.blob

        try:
            ocr_text = extract_text_from_image_bytes(
                image_bytes
            )

            if ocr_text:
                ocr_parts.append(
                    ocr_text
                )

        except Exception:
            continue

    text_parts.extend(
        ocr_parts
    )

    return "\n".join(text_parts)


def extract_pptx_text(file_bytes):
    presentation = Presentation(
        io.BytesIO(file_bytes)
    )

    text_parts = []

    for slide in presentation.slides:

        # Extract normal slide text
        for shape in slide.shapes:

            if hasattr(shape, "text"):
                text = shape.text.strip()

                if text:
                    text_parts.append(text)

        # Extract and OCR images
        for shape in slide.shapes:

            if shape.shape_type != 13:
                continue

            try:
                image_bytes = shape.image.blob

                ocr_text = extract_text_from_image_bytes(
                    image_bytes
                )

                if ocr_text:
                    text_parts.append(
                        ocr_text
                    )

            except Exception:
                continue

    return "\n".join(text_parts)


def extract_xlsx_text(file_bytes):
    workbook = load_workbook(
        io.BytesIO(file_bytes),
        data_only=True
    )

    text_parts = []

    for worksheet in workbook.worksheets:

        # Extract normal cell text
        for row in worksheet.iter_rows():

            row_values = []

            for cell in row:

                if cell.value is not None:
                    row_values.append(
                        str(cell.value)
                    )

            if row_values:
                text_parts.append(
                    " | ".join(row_values)
                )

        # Extract and OCR embedded images
        for image in worksheet._images:

            try:
                image_bytes = image._data()

                ocr_text = extract_text_from_image_bytes(
                    image_bytes
                )

                if ocr_text:
                    text_parts.append(
                        ocr_text
                    )

            except Exception:
                continue

    return "\n".join(text_parts)


def extract_csv_text(file_bytes):
    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError(
            "The uploaded .csv file must be valid UTF-8 text."
        )

    reader = csv.reader(
        io.StringIO(text)
    )

    rows = []

    for row in reader:
        values = [
            value.strip()
            for value in row
            if value.strip()
        ]

        if values:
            rows.append(
                " | ".join(values)
            )

    return "\n".join(rows)


def extract_markdown_text(file_bytes):
    try:
        return file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError(
            "The uploaded .md file must be valid UTF-8 text."
        )


def extract_html_text(file_bytes, base_dir=None):
    import base64
    import os
    import urllib.request
    from urllib.parse import urljoin

    html = file_bytes.decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove elements that should not contribute text
    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    text_parts = []

    # --------------------------------------------------
    # 1. Extract normal HTML text
    # --------------------------------------------------

    normal_text = soup.get_text(
        "\n",
        strip=True
    )

    if normal_text:
        text_parts.append(
            normal_text
        )

    # --------------------------------------------------
    # 2. Extract and OCR images
    # --------------------------------------------------

    for image in soup.find_all("img"):

        image_source = image.get("src")

        if not image_source:
            continue

        image_bytes = None

        try:

            # ------------------------------------------
            # CASE 1: Base64 / Data URI image
            # ------------------------------------------

            if image_source.startswith(
                "data:image/"
            ):

                header, encoded_data = (
                    image_source.split(
                        ",",
                        1
                    )
                )

                image_bytes = base64.b64decode(
                    encoded_data
                )

            # ------------------------------------------
            # CASE 2: HTTP / HTTPS image
            # ------------------------------------------

            elif image_source.startswith(
                "http://"
            ) or image_source.startswith(
                "https://"
            ):

                request = urllib.request.Request(
                    image_source,
                    headers={
                        "User-Agent":
                        "PrivateSearchEngine/1.0"
                    }
                )

                with urllib.request.urlopen(
                    request,
                    timeout=10
                ) as response:

                    content_type = (
                        response.headers.get(
                            "Content-Type",
                            ""
                        ).lower()
                    )

                    if not content_type.startswith(
                        "image/"
                    ):
                        continue

                    max_size = 5 * 1024 * 1024

                    image_bytes = response.read(
                        max_size + 1
                    )

                    if len(image_bytes) > max_size:
                        continue

                        # ------------------------------------------
            # CASE 3: Local / relative image path
            # ------------------------------------------

            else:

                if base_dir is None:
                    continue

                from pathlib import Path
                from urllib.parse import unquote

                relative_path = unquote(
                    image_source
                )

                local_path = (
                    Path(base_dir) / relative_path
                ).resolve()

                base_path = (
                    Path(base_dir)
                    .resolve()
                )

                # Make sure the image stays inside
                # the HTML document's directory.
                try:
                    local_path.relative_to(
                        base_path
                    )
                except ValueError:
                    continue

                if local_path.is_file():

                    with open(
                        local_path,
                        "rb"
                    ) as image_file:

                        image_bytes = (
                            image_file.read()
                        )

                else:
                    continue

            # ------------------------------------------
            # OCR
            # ------------------------------------------

            if image_bytes:

                ocr_text = (
                    extract_text_from_image_bytes(
                        image_bytes
                    )
                )

                if ocr_text:

                    text_parts.append(
                        ocr_text
                    )

        except Exception:
            continue

    return "\n".join(text_parts)


def extract_html_zip_text(file_bytes):
    with tempfile.TemporaryDirectory() as temp_directory:

        temp_path = Path(temp_directory)

        # ------------------------------------------
        # Extract ZIP safely
        # ------------------------------------------

        with zipfile.ZipFile(
            io.BytesIO(file_bytes)
        ) as zip_file:

            for member in zip_file.infolist():

                member_path = (
                    temp_path / member.filename
                ).resolve()

                try:
                    member_path.relative_to(
                        temp_path.resolve()
                    )
                except ValueError:
                    continue

                if member.is_dir():
                    member_path.mkdir(
                        parents=True,
                        exist_ok=True
                    )
                else:
                    member_path.parent.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    with zip_file.open(
                        member
                    ) as source:

                        with open(
                            member_path,
                            "wb"
                        ) as destination:

                            destination.write(
                                source.read()
                            )

        # ------------------------------------------
        # Find HTML files
        # ------------------------------------------

        html_files = list(
            temp_path.rglob("*.html")
        )

        html_files.extend(
            temp_path.rglob("*.htm")
        )

        if not html_files:
            raise ValueError(
                "The ZIP file does not contain an HTML file."
            )

        if len(html_files) > 1:
            raise ValueError(
                "The ZIP file must contain only one HTML file."
            )

        html_file = html_files[0]

        # ------------------------------------------
        # Read HTML
        # ------------------------------------------

        html_bytes = html_file.read_bytes()

        # ------------------------------------------
        # Extract HTML text + OCR local images
        # ------------------------------------------

        return extract_html_text(
            html_bytes,
            base_dir=html_file.parent
        )