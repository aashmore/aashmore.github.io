import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "physics-gre" / "pdfs"
OUT = ROOT / "physics-gre" / "py130-question-bank"
RESOLUTION = 220

SOURCES = {
    "1986": ("1986_exam.pdf", "1986 released exam", True),
    "1992": ("1992_exam.pdf", "1992 released exam", True),
    "1996": ("1996_exam.pdf", "1996 released exam", True),
    "2001": ("2001_exam.pdf", "2001 released exam", False),
    "2008": ("2008_exam.pdf", "2008 released exam", False),
    "2017": ("2017_exam.pdf", "2017 released exam", False),
    "current": ("practice-book-physics.pdf", "Current practice book", False),
    "sample-1": ("textbook.pdf", "Study guide sample exam 1", False),
    "sample-2": ("textbook.pdf", "Study guide sample exam 2", False),
    "sample-3": ("textbook.pdf", "Study guide sample exam 3", False),
}

# source|question|PDF page|topic|fit
RAW_ITEMS = r"""
1986|1|5|Dynamics|borderline
1986|2|5|Gravitation|borderline
1986|5|5|Momentum|direct
1986|6|6|Kinematics|direct
1986|7|6|Statics|direct
1986|8|6|Work and energy|direct
1986|34|11|Work and energy|direct
1986|37|11|Circular motion|direct
1986|44|13|Momentum|direct
1986|60|15|Oscillations|borderline
1986|61|16|Momentum|borderline
1986|62|16|Momentum|borderline
1986|75|17|Gravitation|direct
1986|76|18|Rotation|direct
1986|77|18|Oscillations|borderline
1986|93|21|Dynamics|direct
1986|97|23|Rotation|direct
1992|4|5|Gravitation|direct
1992|5|5|Gravitation|direct
1992|6|6|Statics|direct
1992|8|7|Rotation|direct
1992|19|10|Gravitation|direct
1992|40|14|Rotation|direct
1992|41|14|Work and energy|direct
1992|42|14|Rotation|direct
1992|45|15|Work and energy|direct
1992|48|16|Experimental methods|direct
1992|61|18|Oscillations|borderline
1992|66|19|Work and energy|direct
1992|74|21|Oscillations|borderline
1992|82|23|Rotation|direct
1992|87|25|Gravitation|borderline
1992|93|26|Kinematics|direct
1992|100|28|Statics|direct
1996|5|16|Circular motion|direct
1996|6|16|Work and energy|direct
1996|7|16|Momentum|direct
1996|20|22|Momentum|borderline
1996|21|24|Oscillations|borderline
1996|22|24|Gravitation|direct
1996|23|24|Gravitation|borderline
1996|27|26|Experimental methods|direct
1996|31|28|Dynamics|borderline
1996|32|30|Rotation|direct
1996|44|32|Kinematics|direct
1996|65|40|Momentum|direct
1996|66|40|Gravitation|direct
1996|83|50|Circular motion|borderline
1996|92|62|Oscillations|borderline
1996|93|64|Oscillations|borderline
2001|1|12|Kinematics|direct
2001|2|12|Circular motion|direct
2001|3|12|Gravitation|direct
2001|4|12|Momentum|direct
2001|22|22|Gravitation|direct
2001|23|22|Circular motion|direct
2001|24|24|Kinematics|direct
2001|25|26|Rotation|direct
2001|26|26|Work and energy|direct
2001|54|40|Momentum|direct
2001|55|40|Momentum|direct
2001|72|48|Dynamics|borderline
2001|73|48|Dynamics|direct
2001|89|58|Rotation|direct
2001|90|60|Oscillations|borderline
2001|91|62|Rotation|direct
2008|1|12|Kinematics|direct
2008|2|12|Kinematics|direct
2008|9|16|Gravitation|direct
2008|10|16|Work and energy|direct
2008|28|26|Work and energy|direct
2008|29|26|Momentum|direct
2008|53|44|Gravitation|direct
2008|54|44|Gravitation|direct
2008|56|44|Kinematics|direct
2008|57|46|Dynamics|direct
2008|58|48|Dynamics|direct
2008|59|48|Dynamics|borderline
2008|80|62|Oscillations|borderline
2008|81|64|Rotation|direct
2008|84|66|Rotation|direct
2008|99|82|Circular motion|direct
2017|1|10|Dynamics|direct
2017|2|10|Momentum|direct
2017|3|12|Oscillations|borderline
2017|17|16|Gravitation|direct
2017|18|16|Gravitation|direct
2017|19|16|Work and energy|direct
2017|42|34|Experimental methods|direct
2017|46|36|Work and energy|direct
2017|48|36|Rotation|direct
2017|49|36|Kinematics|direct
2017|65|52|Rotation|direct
2017|66|52|Oscillations|borderline
2017|79|64|Dynamics|direct
2017|80|66|Gravitation|direct
2017|87|70|Work and energy|direct
2017|88|72|Kinematics|direct
2017|89|72|Dynamics|borderline
2017|90|74|Work and energy|direct
current|1|9|Momentum|direct
current|2|9|Oscillations|borderline
current|14|11|Gravitation|direct
current|15|11|Gravitation|direct
current|16|11|Work and energy|direct
current|36|15|Experimental methods|direct
current|39|16|Work and energy|direct
current|41|16|Rotation|direct
current|51|20|Rotation|direct
current|62|22|Dynamics|direct
current|67|23|Kinematics|direct
current|68|23|Dynamics|borderline
current|69|23|Work and energy|direct
sample-1|1|186|Circular motion|direct
sample-1|2|186|Momentum|direct
sample-1|9|187|Gravitation|borderline
sample-1|10|187|Rotation|direct
sample-1|24|190|Statics|direct
sample-1|29|190|Gravitation|borderline
sample-1|35|191|Rotation|direct
sample-1|47|193|Work and energy|direct
sample-1|55|194|Kinematics|direct
sample-1|56|194|Momentum|borderline
sample-1|58|195|Rotation|direct
sample-1|73|197|Rotation|borderline
sample-1|74|197|Rotation|direct
sample-2|1|204|Dynamics|borderline
sample-2|3|204|Circular motion|direct
sample-2|7|204|Dynamics|direct
sample-2|19|207|Momentum|direct
sample-2|28|209|Gravitation|direct
sample-2|29|210|Work and energy|direct
sample-2|49|213|Rotation|direct
sample-2|56|214|Work and energy|direct
sample-2|57|214|Statics|direct
sample-2|65|216|Statics|direct
sample-2|76|219|Kinematics|direct
sample-2|93|222|Circular motion|direct
sample-2|100|223|Rotation|direct
sample-3|4|226|Work and energy|direct
sample-3|8|227|Rotation|borderline
sample-3|11|227|Gravitation|borderline
sample-3|17|228|Kinematics|direct
sample-3|18|228|Momentum|direct
sample-3|25|230|Rotation|borderline
sample-3|44|233|Rotation|direct
sample-3|47|234|Oscillations|borderline
sample-3|51|234|Dynamics|direct
sample-3|58|235|Momentum|direct
sample-3|82|238|Rotation|direct
sample-3|94|240|Circular motion|direct
sample-3|96|240|Gravitation|borderline
sample-3|98|241|Work and energy|direct
"""

# Questions whose prompt explicitly depends on text before its numbered line.
SHARED_STEM_TOP = {
    ("1986", 34): 55,
    ("1986", 61): 55,
    ("1986", 62): 55,
    ("1992", 4): 55,
    ("1992", 5): 55,
    ("1992", 41): 55,
    ("1992", 42): 55,
}

# PDF-point boxes for OCR misses in the 1996 scan.
MANUAL_BOXES = {
    ("1996", 20): (290, 195, 578, 390),
    ("1996", 31): (290, 20, 578, 385),
    ("1996", 44): (290, 250, 578, 510),
    ("1996", 65): (290, 20, 578, 325),
    ("1996", 66): (290, 305, 578, 565),
    ("current", 14): (18, 145, 313, 430),
    ("current", 15): (18, 385, 313, 765),
    ("current", 16): (299, 42, 594, 270),
}


def parse_items():
    items = []
    for line in RAW_ITEMS.strip().splitlines():
        source, q, page, topic, fit = line.split("|")
        items.append(
            {"source": source, "question": int(q), "page": int(page), "topic": topic, "fit": fit}
        )
    return items


def dedupe(points, tolerance=2.0):
    result = []
    for point in sorted(points, key=lambda p: (p[1], p[0])):
        if not any(abs(point[0] - x) < tolerance and abs(point[1] - y) < tolerance for x, y in result):
            result.append(point)
    return result


def text_question_starts(page):
    starts = defaultdict(list)
    words = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=False)
    for word in words:
        match = re.fullmatch(r"(\d{1,3})\.", word["text"])
        if match:
            q = int(match.group(1))
            if 1 <= q <= 100:
                starts[q].append((float(word["x0"]), float(word["top"])))
    return {q: dedupe(points) for q, points in starts.items()}


def ocr_question_starts(source):
    import json

    path = ROOT / "tmp" / "pdfs" / f"{source}_ocr.json"
    data = json.loads(path.read_text(encoding="utf-8"))["pages"]
    pages = {}
    for page in data:
        starts = defaultdict(list)
        for line in page["lines"]:
            text = line["text"].strip()
            for match in re.finditer(r"(?:^|\D)(\d{1,3})\.", text):
                q = int(match.group(1))
                if 1 <= q <= 100:
                    box = line["box"]
                    starts[q].append((float(box[0][0]) * 72 / 96, float(box[0][1]) * 72 / 96))
        pages[int(page["page"])] = {q: dedupe(points, 4.0) for q, points in starts.items()}
    return pages


def ocr_question_boxes(source):
    import json

    data = json.loads((ROOT / "tmp" / "pdfs" / f"{source}_questions.json").read_text(encoding="utf-8"))["questions"]
    boxes = {}
    for item in data:
        box = item["bbox"]
        boxes[(int(item["page"]), int(item["number"]))] = tuple(float(value) * 72 / 96 for value in box)
    return boxes


def choose_start(starts, q, width):
    points = starts.get(q, [])
    if not points:
        raise ValueError(f"Could not find question {q}")
    plausible = [(x, y) for x, y in points if x < width - 25 and y > 25]
    return min(plausible or points, key=lambda p: (p[1], p[0]))


def crop_box(page, starts, q, source, scanned_box=None):
    width, height = float(page.width), float(page.height)
    manual = MANUAL_BOXES.get((source, q))
    if manual:
        return manual
    if scanned_box:
        x0, y0, x1, y1 = scanned_box
        left_column = x0 < width / 2
        left = 8 if left_column else width / 2 - 7
        right = width / 2 + 7 if left_column else width - 8
        top = max(42, y0 - 90)
        if (source, q) in SHARED_STEM_TOP:
            top = SHARED_STEM_TOP[(source, q)]
        return (left, top, right, min(height - 2, y1 + 8))

    x, y = choose_start(starts, q, width)
    left_column = x < width / 2
    x0 = 18 if left_column else width / 2 - 7
    x1 = width / 2 + 7 if left_column else width - 18

    same_column_next = []
    for other_q, points in starts.items():
        if other_q == q:
            continue
        for ox, oy in points:
            if (ox < width / 2) == left_column and oy > y + 8:
                same_column_next.append(oy)
    next_y = min(same_column_next) if same_column_next else height - 35

    # Figures are often placed above the numbered line. The generous lead-in is
    # deliberate; a little overlap is preferable to losing a diagram or stem.
    top = max(42, y - 112)
    if (source, q) in SHARED_STEM_TOP:
        top = SHARED_STEM_TOP[(source, q)]
    bottom = min(height - 30, next_y - 3)
    if bottom - top < 115:
        bottom = min(height - 30, top + 170)
    return (x0, top, x1, bottom)


def make_contact_sheet(source_dir, output):
    files = sorted(source_dir.glob("*.png"))
    thumb_w, thumb_h = 300, 390
    columns = 4
    rows = (len(files) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + 34)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w - 12, thumb_h - 12))
        col, row = index % columns, index // columns
        x = col * thumb_w + (thumb_w - image.width) // 2
        y = row * (thumb_h + 34) + 4
        sheet.paste(image, (x, y))
        draw.text((col * thumb_w + 8, y + thumb_h), path.stem, fill="black", font=font)
    sheet.save(output, quality=90)


def main():
    items = parse_items()
    OUT.mkdir(parents=True, exist_ok=True)
    ocr_cache = {source: ocr_question_starts(source) for source in ("1986", "1992", "1996")}
    ocr_box_cache = {source: ocr_question_boxes(source) for source in ("1986", "1992", "1996")}
    for old_file in OUT.rglob("*.png"):
        old_file.unlink()
    for old_file in OUT.rglob("*.jpg"):
        old_file.unlink()
    pdf_cache = {}
    index_rows = []

    for item in items:
        source = item["source"]
        pdf_name, source_label, scanned = SOURCES[source]
        if pdf_name not in pdf_cache:
            pdf_cache[pdf_name] = pdfplumber.open(PDF_DIR / pdf_name)
        page = pdf_cache[pdf_name].pages[item["page"] - 1]
        starts = ocr_cache[source][item["page"]] if scanned else text_question_starts(page)
        scanned_box = ocr_box_cache[source].get((item["page"], item["question"])) if scanned else None
        box = crop_box(page, starts, item["question"], source, scanned_box)
        source_dir = OUT / source
        source_dir.mkdir(exist_ok=True)
        filename = f"{source}_q{item['question']:03d}_pdf-p{item['page']:03d}_{item['fit']}.png"
        image = page.crop(box).to_image(resolution=RESOLUTION, antialias=True)
        image.save(source_dir / filename)
        index_rows.append(
            {
                "source": source_label,
                "question": item["question"],
                "pdf_page": item["page"],
                "topic": item["topic"],
                "fit": item["fit"],
                "screenshot": f"{source}/{filename}",
                "source_pdf": f"../pdfs/{pdf_name}",
            }
        )

    for pdf in pdf_cache.values():
        pdf.close()

    with (OUT / "index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=index_rows[0].keys())
        writer.writeheader()
        writer.writerows(index_rows)

    source_counts = Counter(row["source"] for row in index_rows)
    topic_counts = Counter(row["topic"] for row in index_rows)
    direct = sum(row["fit"] == "direct" for row in index_rows)
    borderline = len(index_rows) - direct
    lines = [
        "# PY 130 question bank",
        "",
        "This folder contains screenshots of mechanics questions selected from every released/practice exam in `../pdfs/` and from the three sample exams in `textbook.pdf`.",
        "",
        "## Selection guide",
        "",
        "- `direct`: a straightforward fit for calculus-based introductory mechanics.",
        "- `borderline`: still potentially useful, but may involve drag, oscillations, rotating frames, rocket motion, or a slightly more advanced central-force model.",
        "- Question numbers and original PDF page numbers are embedded in each filename.",
        "- Crops intentionally include some preceding space so diagrams and shared stems are not lost.",
        "- `index.csv` is the sortable catalog and links every screenshot to its source PDF.",
        "",
        "## Coverage",
        "",
        f"Total: {len(index_rows)} questions ({direct} direct, {borderline} borderline).",
        "",
    ]
    for name, count in source_counts.items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Topics", ""])
    for topic, count in sorted(topic_counts.items()):
        lines.append(f"- {topic}: {count}")
    lines.extend(
        [
            "",
            "## Scope used",
            "",
            "The selection follows the PY 130 description in the site: translational and rotational kinematics and dynamics, work and energy, conservation laws, and gravitation. Fluids, thermodynamics, waves as a standalone topic, relativity, electromagnetism, optics, atomic physics, and quantum mechanics were excluded.",
            "",
            "These are source excerpts for instructor review. Check the source publication's reuse terms before redistributing them outside the course context.",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")

    contact_dir = OUT / "contact-sheets"
    contact_dir.mkdir(exist_ok=True)
    for source in SOURCES:
        make_contact_sheet(OUT / source, contact_dir / f"{source}.jpg")

    print(f"Created {len(index_rows)} screenshots in {OUT}")


if __name__ == "__main__":
    main()
