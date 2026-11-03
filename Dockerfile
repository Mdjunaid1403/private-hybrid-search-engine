
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Tesseract OCR and language data
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-kan \
    tesseract-ocr-hin \
    tesseract-ocr-mar \
    tesseract-ocr-guj \
    tesseract-ocr-ben \
    tesseract-ocr-mal \
    tesseract-ocr-tam \
    tesseract-ocr-tel \
    tesseract-ocr-pan \
    tesseract-ocr-urd \
    tesseract-ocr-osd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "python -m uvicorn app.api:app --host 0.0.0.0 --port ${PORT:-10000}"]
