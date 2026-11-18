from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber


QUESTION_RE = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+")


def extract(pdf_path: Path) -> dict[str, object]:
    pages: list[dict[str, object]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
            pages.append(
                {
                    "page": page_number,
                    "width": page.width,
                    "height": page.height,
                    "text": text,
                }
            )
    return {"source": str(pdf_path), "pages": pages}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(extract(args.pdf), indent=2, ensure_ascii=True),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
