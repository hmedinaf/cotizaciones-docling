FROM python:3.11-slim

WORKDIR /app

# Tesseract OCR engine + Spanish and English language packs
# poppler-utils provides pdfinfo/pdftoppm required by pdf2image
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-spa \
        tesseract-ocr-eng \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py api.py ./

VOLUME ["/input", "/output"]

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
