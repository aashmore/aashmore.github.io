from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pydeps"))

from rapidocr_onnxruntime import RapidOCR  # noqa: E402


def page_number(path: Path) -> int:
    return int(path.stem.rsplit("-", 1)[-1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    engine = RapidOCR()
    pages = []
    image_paths = list(args.image_dir.glob("page-*.png"))
    image_paths.extend(args.image_dir.glob("page-*.jpg"))
    for image_path in sorted(image_paths, key=page_number):
        result, _ = engine(str(image_path))
        lines = []
        for box, text, score in result or []:
            lines.append({"box": box, "text": text, "score": score})
        pages.append(
            {
                "page": page_number(image_path),
                "image": str(image_path),
                "lines": lines,
                "text": "\n".join(line["text"] for line in lines),
            }
        )
        print(f"{image_path.name}: {len(lines)} lines", flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"pages": pages}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
