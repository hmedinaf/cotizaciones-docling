import os
import sys
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/output"))
DPI = int(os.getenv("DPI", "300"))
OCR_LANG = os.getenv("OCR_LANG", "spa+eng")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".webp"}


def file_to_markdown(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        images = convert_from_path(str(file_path), dpi=DPI)
        pages = []
        for i, image in enumerate(images, 1):
            text = pytesseract.image_to_string(image, lang=OCR_LANG).strip()
            pages.append(f"<!-- page {i} -->\n\n{text}")
        return "\n\n---\n\n".join(pages)
    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang=OCR_LANG).strip()
        return text


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_extensions = {".pdf"} | IMAGE_EXTENSIONS
    input_files = sorted(
        f for f in INPUT_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in all_extensions
    )

    if not input_files:
        print(f"No supported files found in {INPUT_DIR}")
        sys.exit(0)

    print(f"Found {len(input_files)} file(s) to process.")
    errors = []

    for file_path in input_files:
        print(f"Processing: {file_path.name} ...")
        try:
            markdown = file_to_markdown(file_path)
            output_path = OUTPUT_DIR / f"{file_path.stem}.md"
            output_path.write_text(markdown, encoding="utf-8")
            print(f"  Saved -> {output_path.name}")
        except Exception as exc:
            print(f"  ERROR: {exc}")
            errors.append(file_path.name)

    if errors:
        print(f"\nFailed to process {len(errors)} file(s): {', '.join(errors)}")
        sys.exit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
