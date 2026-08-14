"""
build_combined_pdf.py

Combines individual question PDFs into one PDF, grouped by topic
(in topic-number order). Each topic starts with a blank page showing
just the topic title, followed by all the question PDFs for that topic
(in the order they appear in paper2Data).

Usage:
    python build_combined_pdf.py

Requirements:
    pip install pypdf reportlab --break-system-packages

Expected folder layout (edit PDF_DIR below if yours differs):
    ./paper2_data.json      <- produced by export_to_json.js
    ./pdfs/                 <- folder containing all the individual question PDFs
        9702_m25_qp_22_Q1_Physical_quantities_and_units_1_3_2.pdf
        9702_m25_qp_22_Q2_Forces_density_and_pressure.pdf
        ...
"""

import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---- Config -----------------------------------------------------
DATA_JSON = Path("paper2_data.json")
PDF_DIR = Path("pdfs")          # folder holding all the question PDFs
OUTPUT_PDF = Path("combined_by_topic.pdf")
TITLE_PAGE_PDF = Path("_title_page_tmp.pdf")  # scratch file, deleted at the end
# -------------------------------------------------------------------


def make_title_page(text: str, out_path: Path):
    """Create a single-page PDF with `text` centered on an otherwise blank page."""
    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height / 2, text)
    c.showPage()
    c.save()


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    topic_meta = data["topicMeta"]
    questions = data["paper2Data"]

    # Group questions by topic
    by_topic = {}
    for q in questions:
        by_topic.setdefault(q["topic"], []).append(q)

    # Sort topics numerically (keys are strings like '1', '2', ..., '11')
    topic_order = sorted(by_topic.keys(), key=lambda k: int(k))

    writer = PdfWriter()
    missing = []

    for topic_id in topic_order:
        topic_name = topic_meta.get(topic_id, f"Topic {topic_id}")

        # 1. Blank title page for this topic
        make_title_page(f"Topic {topic_id}\n{topic_name}".replace("\n", " — "), TITLE_PAGE_PDF)
        title_reader = PdfReader(str(TITLE_PAGE_PDF))
        for page in title_reader.pages:
            writer.add_page(page)

        # 2. All question PDFs under this topic, in listed order
        for q in by_topic[topic_id]:
            pdf_path = PDF_DIR / q["pdf"]
            if not pdf_path.exists():
                missing.append(str(pdf_path))
                continue
            reader = PdfReader(str(pdf_path))
            for page in reader.pages:
                writer.add_page(page)

    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    if TITLE_PAGE_PDF.exists():
        TITLE_PAGE_PDF.unlink()

    print(f"Done. Wrote {OUTPUT_PDF} ({len(writer.pages)} pages).")
    if missing:
        print(f"\nWARNING: {len(missing)} PDF(s) not found and skipped:")
        for m in missing:
            print("  -", m)


if __name__ == "__main__":
    main()
