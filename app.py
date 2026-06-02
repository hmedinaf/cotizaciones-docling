import os
import sys
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/output"))
DPI = int(os.getenv("DPI", "300"))
OCR_LANG = os.getenv("OCR_LANG", "spa+eng")


def pdf_to_markdown(pdf_path: Path) -> str:
    images = convert_from_path(str(pdf_path), dpi=DPI)
    pages = []
    for i, image in enumerate(images, 1):
        text = pytesseract.image_to_string(image, lang=OCR_LANG).strip()
        pages.append(f"<!-- page {i} -->\n\n{text}")
    return "\n\n---\n\n".join(pages)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        sys.exit(0)

    print(f"Found {len(pdf_files)} PDF(s) to process.")
    errors = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name} ...")
        try:
            markdown = pdf_to_markdown(pdf_path)
            output_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
            output_path.write_text(markdown, encoding="utf-8")
            print(f"  Saved -> {output_path.name}")
        except Exception as exc:
            print(f"  ERROR: {exc}")
            errors.append(pdf_path.name)

    if errors:
        print(f"\nFailed to process {len(errors)} file(s): {', '.join(errors)}")
        sys.exit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
