from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


NUMBER_RE = re.compile(r"^\s*(\d{1,3})[.)]\s*")


def bounds(box: list[list[float]]) -> tuple[float, float, float, float]:
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]
    return min(xs), min(ys), max(xs), max(ys)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ocr_json", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.ocr_json.read_text(encoding="utf-8"))
    questions = []
    for page in data["pages"]:
        image_path = Path(page["image"])
        with Image.open(image_path) as image:
            width, height = image.size
        lines = []
        starts = []
        for line in page["lines"]:
            x0, y0, x1, y1 = bounds(line["box"])
            item = {**line, "x0": x0, "y0": y0, "x1": x1, "y1": y1}
            lines.append(item)
            match = NUMBER_RE.match(line["text"])
            if match:
                number = int(match.group(1))
                column = 0 if x0 < width / 2 else 1
                left_edge = 0 if column == 0 else width / 2
                if 1 <= number <= 100 and x0 - left_edge < width * 0.13:
                    starts.append({"number": number, "column": column, "y0": y0, "x0": x0})

        for start in starts:
            next_y = min(
                (
                    other["y0"]
                    for other in starts
                    if other["column"] == start["column"] and other["y0"] > start["y0"] + 3
                ),
                default=height - 35,
            )
            left = 10 if start["column"] == 0 else width / 2
            right = width / 2 if start["column"] == 0 else width - 10
            selected = [
                line["text"]
                for line in lines
                if line["x0"] >= left - 5
                and line["x1"] <= right + 5
                and line["y0"] >= start["y0"] - 3
                and line["y0"] < next_y - 2
            ]
            questions.append(
                {
                    "number": start["number"],
                    "page": page["page"],
                    "image": str(image_path),
                    "bbox": [left, max(0, start["y0"] - 5), right, next_y - 2],
                    "text": "\n".join(selected),
                }
            )

    args.output.write_text(json.dumps({"questions": questions}, indent=2), encoding="utf-8")
    print(f"{args.ocr_json.name}: found {len(questions)} question starts")


if __name__ == "__main__":
    main()
