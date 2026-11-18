from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber


NUMBER_RE = re.compile(r"^(\d{1,3})[.)]$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    questions = []
    with pdfplumber.open(args.pdf) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(
                x_tolerance=2,
                y_tolerance=3,
                keep_blank_chars=False,
                use_text_flow=False,
            )
            starts = []
            for word in words:
                match = NUMBER_RE.match(word["text"])
                if not match:
                    continue
                number = int(match.group(1))
                if not 1 <= number <= 100 or word["top"] < 45:
                    continue
                column = 0 if word["x0"] < page.width / 2 else 1
                left_edge = 0 if column == 0 else page.width / 2
                if word["x0"] - left_edge > 65:
                    continue
                starts.append(
                    {
                        "number": number,
                        "column": column,
                        "top": float(word["top"]),
                        "x0": float(word["x0"]),
                    }
                )

            for start in starts:
                next_tops = [
                    other["top"]
                    for other in starts
                    if other["column"] == start["column"]
                    and other["top"] > start["top"] + 2
                ]
                bottom = min(next_tops) - 3 if next_tops else page.height - 32
                left = 18 if start["column"] == 0 else page.width / 2
                right = page.width / 2 if start["column"] == 0 else page.width - 18
                bbox = [float(left), max(0.0, start["top"] - 4), float(right), float(bottom)]
                crop = page.crop(tuple(bbox), strict=False)
                questions.append(
                    {
                        "number": start["number"],
                        "page": page_number,
                        "bbox": bbox,
                        "text": crop.extract_text(x_tolerance=2, y_tolerance=3) or "",
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"source": str(args.pdf), "questions": questions}, indent=2), encoding="utf-8")
    print(f"{args.pdf.name}: found {len(questions)} question starts")


if __name__ == "__main__":
    main()
