"""
build_paper1_24_25.py

Build a combined PDF of 9702 Paper 1 (Multiple Choice) question papers for a
given year range, WITH answer keys, containing:
  - a designed cover page
  - a table of contents (with page numbers)
  - a divider page before each paper
  - the questions, then the official mark scheme, immediately after each paper
  - PDF bookmarks for navigation

All papers are the official full question papers; each is followed by its
official mark scheme (9702_*_ms_1x.pdf). If a mark scheme is missing, a note
page is inserted instead.

Usage:
    python3 build_paper1_24_25.py            # build 24/25 (default)
    python3 build_paper1_24_25.py 22_23      # build 22/23

Output:
    9702 Paper1 24-25 合集.pdf   /   9702 Paper1 22-23 合集.pdf
"""

import math
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
TMP = ROOT / "_paper1_collection_tmp"

PAGE_W, PAGE_H = A4  # 595.0 x 842.0 pt


# ----------------------------------------------------------------------------
# Paper lists (in final order) — every one has an official qp + ms PDF alongside
# ----------------------------------------------------------------------------
PAPERS_24_25 = [
    ("9702_m24_qp_12", "March 2024  ·  Paper 12"),
    ("9702_s24_qp_11", "June 2024  ·  Paper 11"),
    ("9702_s24_qp_12", "June 2024  ·  Paper 12"),
    ("9702_s24_qp_13", "June 2024  ·  Paper 13"),
    ("9702_w24_qp_11", "November 2024  ·  Paper 11"),
    ("9702_w24_qp_12", "November 2024  ·  Paper 12"),
    ("9702_w24_qp_13", "November 2024  ·  Paper 13"),
    ("9702_m25_qp_12", "March 2025  ·  Paper 12"),
    ("9702_s25_qp_11", "June 2025  ·  Paper 11"),
    ("9702_s25_qp_12", "June 2025  ·  Paper 12"),
    ("9702_s25_qp_13", "June 2025  ·  Paper 13"),
    ("9702_w25_qp_11", "November 2025  ·  Paper 11"),
    ("9702_w25_qp_12", "November 2025  ·  Paper 12"),
    ("9702_w25_qp_13", "November 2025  ·  Paper 13"),
    ("9702_w25_qp_14", "November 2025  ·  Paper 14"),
]

PAPERS_22_23 = [
    ("9702_m22_qp_12", "March 2022  ·  Paper 12"),
    ("9702_s22_qp_11", "June 2022  ·  Paper 11"),
    ("9702_s22_qp_12", "June 2022  ·  Paper 12"),
    ("9702_s22_qp_13", "June 2022  ·  Paper 13"),
    ("9702_w22_qp_11", "November 2022  ·  Paper 11"),
    ("9702_w22_qp_12", "November 2022  ·  Paper 12"),
    ("9702_w22_qp_13", "November 2022  ·  Paper 13"),
    ("9702_m23_qp_12", "March 2023  ·  Paper 12"),
    ("9702_s23_qp_11", "June 2023  ·  Paper 11"),
    ("9702_s23_qp_12", "June 2023  ·  Paper 12"),
    ("9702_s23_qp_13", "June 2023  ·  Paper 13"),
    ("9702_w23_qp_11", "November 2023  ·  Paper 11"),
    ("9702_w23_qp_12", "November 2023  ·  Paper 12"),
    ("9702_w23_qp_13", "November 2023  ·  Paper 13"),
]

COLLECTIONS = {
    "24_25": dict(
        year_slash="24 / 25",
        subtitle="MULTIPLE CHOICE  ·  COMPLETE COLLECTION 2024–2025",
        papers=PAPERS_24_25,
        out="9702 Paper1 24-25 合集.pdf",
    ),
    "22_23": dict(
        year_slash="22 / 23",
        subtitle="MULTIPLE CHOICE  ·  COMPLETE COLLECTION 2022–2023",
        papers=PAPERS_22_23,
        out="9702 Paper1 22-23 合集.pdf",
    ),
}


def ms_path(qp: Path) -> Path:
    return qp.with_name(qp.name.replace("_qp_", "_ms_"))


# ----------------------------------------------------------------------------
# Cover
# ----------------------------------------------------------------------------
def make_cover(out: Path, year_slash: str, subtitle: str, n_papers: int):
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = PAGE_W, PAGE_H
    c.setTitle(f"9702 Paper 1 {year_slash.replace('/', '-')}")

    NAVY_TOP = HexColor("#200A26")
    NAVY_BOT = HexColor("#08030C")
    GRID = HexColor("#30143A")
    MAGENTA = HexColor("#F472B6")
    CYAN = HexColor("#22D3EE")
    WHITE = HexColor("#F8FAFC")
    MUTED = HexColor("#9BA3AF")

    def centered(text, cx, y, size, font, color, space=0.0, alpha=1.0):
        c.setFont(font, size)
        c.setFillColor(color)
        c.setFillAlpha(alpha)
        widths = [c.stringWidth(ch, font, size) for ch in text]
        total = sum(widths) + space * max(0, len(text) - 1)
        x = cx - total / 2.0
        for ch, cw in zip(text, widths):
            c.drawString(x, y, ch)
            x += cw + space
        c.setFillAlpha(1.0)

    # 1. vertical gradient background (top light -> bottom dark)
    c.linearGradient(0, h, 0, 0, [NAVY_TOP, NAVY_BOT], extend=True)

    # 2. faint grid
    c.setStrokeColor(GRID)
    c.setStrokeAlpha(0.55)
    c.setLineWidth(0.5)
    for x in range(0, int(w) + 1, 48):
        c.line(x, 0, x, h)
    for y in range(0, int(h) + 1, 48):
        c.line(0, y, w, y)
    c.setStrokeAlpha(1.0)

    # 3. giant ghost "9702" behind the title
    centered("9702", w / 2, 520, 320, "Helvetica-Bold", MAGENTA, 6, alpha=0.06)

    # 4. particle-collision rings (top-right)
    cx, cy = w + 30, h + 20
    for i, r in enumerate([60, 110, 160, 210]):
        c.setStrokeColor(MAGENTA)
        c.setStrokeAlpha(max(0.08, 0.5 - i * 0.13))
        c.setLineWidth(1.2)
        c.circle(cx, cy, r, stroke=1, fill=0)
    c.setStrokeAlpha(1.0)
    for ang, r, rr in [(20, 160, 4), (45, 110, 3), (160, 160, 3), (250, 110, 5), (320, 210, 3), (80, 60, 2)]:
        px = cx + r * math.cos(math.radians(ang))
        py = cy + r * math.sin(math.radians(ang))
        c.setFillColor(CYAN)
        c.setFillAlpha(0.9)
        c.circle(px, py, rr, stroke=0, fill=1)
    c.setFillAlpha(1.0)
    c.setFillColor(CYAN)
    c.circle(cx, cy - 160, 4.5, stroke=0, fill=1)

    # 5. scattered particle dust
    particles = [
        (70, 700, 2.0, MAGENTA, 0.5), (120, 660, 1.5, CYAN, 0.6), (55, 620, 2.4, MAGENTA, 0.32),
        (150, 730, 1.2, CYAN, 0.5), (95, 560, 1.8, MAGENTA, 0.38), (140, 520, 1.0, CYAN, 0.5),
        (60, 470, 2.2, MAGENTA, 0.28), (185, 600, 1.4, CYAN, 0.42), (40, 380, 1.6, MAGENTA, 0.35),
        (95, 300, 1.2, CYAN, 0.5), (150, 260, 2.0, MAGENTA, 0.4), (70, 210, 1.4, CYAN, 0.5),
        (525, 700, 1.5, MAGENTA, 0.4), (500, 560, 1.2, CYAN, 0.5), (540, 460, 1.9, MAGENTA, 0.3),
        (525, 300, 1.4, CYAN, 0.45), (560, 210, 1.5, MAGENTA, 0.4),
    ]
    for px, py, pr, pc, pa in particles:
        c.setFillColor(pc)
        c.setFillAlpha(pa)
        c.circle(px, py, pr, stroke=0, fill=1)
    c.setFillAlpha(1.0)

    # 6. sine-wave ribbon (bottom)
    amp, period, yb = 30.0, 150.0, 140.0
    x0, x1 = 40.0, w - 40.0
    steps = 240
    pts = [(x0 + (x1 - x0) * i / steps, yb + amp * math.sin(2 * math.pi * ((x0 + (x1 - x0) * i / steps) - x0) / period))
           for i in range(steps + 1)]
    baseline = yb - amp - 15
    fillp = c.beginPath()
    fillp.moveTo(pts[0][0], baseline)
    for x, y in pts:
        fillp.lineTo(x, y)
    fillp.lineTo(pts[-1][0], baseline)
    fillp.close()
    c.setFillColor(MAGENTA)
    c.setFillAlpha(0.10)
    c.drawPath(fillp, stroke=0, fill=1)
    c.setFillAlpha(1.0)
    curve = c.beginPath()
    curve.moveTo(pts[0][0], pts[0][1])
    for x, y in pts[1:]:
        curve.lineTo(x, y)
    c.setStrokeColor(CYAN)
    c.setStrokeAlpha(0.95)
    c.setLineWidth(2.2)
    c.drawPath(curve, stroke=1, fill=0)
    c.setStrokeAlpha(1.0)

    # 7. accent bars (top teal, bottom amber)
    c.setFillColor(MAGENTA)
    c.rect(0, h - 6, w, 6, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.rect(0, 0, w, 4, stroke=0, fill=1)

    # 8. eyebrow
    centered("CAMBRIDGE INTERNATIONAL  ·  AS & A LEVEL PHYSICS", w / 2, 758, 10.5, "Helvetica-Bold", MAGENTA, 2.5)

    # 9. glowing title
    for scale, alpha in [(1.19, 0.06), (1.11, 0.13), (1.05, 0.24)]:
        c.setFont("Helvetica-Bold", 150 * scale)
        c.setFillColor(MAGENTA)
        c.setFillAlpha(alpha)
        c.drawCentredString(w / 2, 585, "9702")
    c.setFillAlpha(1.0)
    centered("9702", w / 2, 585, 150, "Helvetica-Bold", WHITE, 4)

    centered("PAPER 1", w / 2, 478, 46, "Helvetica-Bold", WHITE, 10)

    # 10. accent rule
    c.setStrokeColor(CYAN)
    c.setLineWidth(3)
    c.setLineCap(1)
    c.line(w / 2 - 70, 432, w / 2 + 70, 432)

    # 11. year range
    centered(year_slash, w / 2, 350, 72, "Helvetica-Bold", CYAN, 8)

    # 12. subtitle + badge
    centered(subtitle, w / 2, 274, 12, "Helvetica", MUTED, 2)
    badge_w, badge_h, badge_r = 210, 30, 15
    bx, by = w / 2 - badge_w / 2, 206
    c.setFillColor(CYAN)
    c.roundRect(bx, by, badge_w, badge_h, badge_r, stroke=0, fill=1)
    c.setFillColor(NAVY_BOT)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawCentredString(w / 2, by + badge_h / 2 - 4, "WITH ANSWER KEYS")

    # 13. footer
    centered(f"PHYSICS (9702)   ·   {n_papers} PAPERS", w / 2, 58, 9, "Helvetica", MUTED, 2)

    c.showPage()
    c.save()


# ----------------------------------------------------------------------------
def make_divider(out: Path, code: str, label: str):
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = PAGE_W, PAGE_H
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h / 2 + 14, label)
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h / 2 - 22, code)
    c.showPage()
    c.save()


def make_missing_note(out: Path, code: str):
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = PAGE_W, PAGE_H
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h / 2 + 10, "Mark scheme not available")
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h / 2 - 20, code)
    c.showPage()
    c.save()


def make_toc(out: Path, entries: list[tuple[str, str, int]]):
    """entries: list of (code, label, start_page_1based)."""
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = PAGE_W, PAGE_H
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2, h - 70, "Contents")
    y = h - 120
    c.setFont("Helvetica", 12)
    for i, (code, label, page) in enumerate(entries, 1):
        c.drawString(70, y, f"{i:>2}.")
        c.drawString(100, y, label)
        c.drawString(350, y, code)
        c.drawRightString(w - 70, y, str(page))
        y -= 22
        if y < 60:
            c.showPage()
            y = h - 70
    c.showPage()
    c.save()


# ----------------------------------------------------------------------------
def build(key: str):
    spec = COLLECTIONS[key]
    papers_spec = spec["papers"]
    TMP.mkdir(exist_ok=True)

    # (code, label, qp_pdf, answer_pdf)  — answer is ms if present, else a note page
    papers = []
    for code, label in papers_spec:
        qp = ROOT / f"{code}.pdf"
        assert qp.exists(), f"missing qp: {qp}"
        ms = ms_path(qp)
        if ms.exists():
            ans = ms
        else:
            ans = TMP / f"note_{code}.pdf"
            make_missing_note(ans, code)
        papers.append((code, label, qp, ans))

    def pdf_pages(p: Path) -> int:
        return len(PdfReader(str(p)).pages)

    dividers = {}
    for code, label, _q, _a in papers:
        d = TMP / f"div_{code}.pdf"
        make_divider(d, code, label)
        dividers[code] = d

    toc_entries = []
    start = 3
    for code, label, qpdf, apdf in papers:
        toc_entries.append((code, label, start))
        start += 1 + pdf_pages(qpdf) + pdf_pages(apdf)

    cover = TMP / "00_cover.pdf"
    toc = TMP / "00_toc.pdf"
    make_cover(cover, spec["year_slash"], spec["subtitle"], len(papers_spec))
    make_toc(toc, toc_entries)

    writer = PdfWriter()
    writer.append(str(cover))
    writer.append(str(toc))
    writer.add_outline_item(f"9702 Paper 1  {spec['year_slash']}", 0)
    writer.add_outline_item("Contents", 1)

    page = 2
    for code, label, qpdf, apdf in papers:
        writer.add_outline_item(f"{code}  —  {label}", page)
        writer.append(str(dividers[code]))
        writer.append(str(qpdf))
        writer.append(str(apdf))
        page += 1 + pdf_pages(qpdf) + pdf_pages(apdf)

    out = ROOT / spec["out"]
    with open(out, "wb") as f:
        writer.write(f)

    total = len(PdfReader(str(out)).pages)
    print(f"Wrote {out.name}  ({total} pages)")
    for code, label, pg in toc_entries:
        print(f"  p.{pg:>3}  {code}   {label}")

    for child in TMP.iterdir():
        child.unlink()
    TMP.rmdir()


if __name__ == "__main__":
    import sys
    key = sys.argv[1] if len(sys.argv) > 1 else "24_25"
    build(key)
