# -*- coding: utf-8 -*-
"""
Slice an IGCSE 0625 Paper 4 (Theory) question paper into one PDF per question.

Each question starts at the top of a fresh page (question number at the left
margin, y~61) and spans full pages until the next question begins. Blank pages
are skipped. Also extracts each question's text (for categorization / titles).

Usage:
    python igcse_theory_slice.py igcse-2024/0625_m24_qp_42.pdf

Outputs:
    igcse-slices/0625_m24_qp_42_Q01.pdf ...
    igcse-data/0625_m24_qp_42.json
    igcse-data/0625_m24_qp_42.questions.txt
"""
import json
import os
import re
import sys

import pymupdf

from igcse_mcq_slice import parse_paper_code

TOP_Y = 100.0          # question numbers sit at y~61; cover blank-page list is lower
LEFT_MARGIN = 62.0


def is_blank_page(page):
    text = page.get_text().strip()
    if "BLANK PAGE" in text.upper():
        return True
    # a page with no meaningful content beyond the header/footer
    compact = re.sub(r"\s+", " ", text)
    compact = compact.replace("© UCLES", "").replace("0625/", "").replace("[Turn over", "")
    compact = re.sub(r"\d+", "", compact).strip()
    return len(compact) < 4


def find_question_starts(doc):
    """Return {qnum: page_index} for each question number 1-12 found at page tops."""
    starts = {}
    for pi in range(1, len(doc)):   # skip cover (page 0)
        page = doc[pi]
        for w in page.get_text("words"):
            x0, y0, word = w[0], w[1], w[4]
            t = word.strip()
            if t.isdigit() and 1 <= int(t) <= 12 and x0 < LEFT_MARGIN and y0 < TOP_Y:
                n = int(t)
                if n not in starts:
                    starts[n] = pi
    return starts


def question_text(doc, pages):
    return "\n".join(doc[pi].get_text().strip() for pi in pages)


def slice_pages(src_doc, page_indices, out_path):
    """Combine a list of source pages into a single clipped PDF (full pages)."""
    new_doc = pymupdf.open()
    for pi in page_indices:
        src_page = src_doc[pi]
        rect = src_page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)
        new_page.show_pdf_page(new_page.rect, src_doc, pi)
    new_doc.save(out_path)
    new_doc.close()


def main(qp_path):
    qp_stem = os.path.splitext(os.path.basename(qp_path))[0]
    paper, paper_full = parse_paper_code(qp_stem)

    src = pymupdf.open(qp_path)
    starts = find_question_starts(src)

    # content pages for each question: from start page up to (next start - 1),
    # excluding blank pages; last question runs to the last non-blank page
    ordered = sorted(starts.items())
    questions = []
    txt_lines = []
    for i, (n, start_pi) in enumerate(ordered):
        end_pi = ordered[i + 1][1] - 1 if i + 1 < len(ordered) else len(src) - 1
        pages = [pi for pi in range(start_pi, end_pi + 1) if not is_blank_page(src[pi])]
        if not pages:
            continue
        pdf_name = f"{qp_stem}_Q{n:02d}.pdf"
        out_path = os.path.join("igcse-slices", pdf_name)
        slice_pages(src, pages, out_path)
        qtxt = question_text(src, pages)
        questions.append({
            "qnum": n,
            "topic": "",
            "title": "",
            "marks": 0,
            "pdf": "igcse-slices/" + pdf_name,
            "parts": [],
        })
        txt_lines.append(f"===== Q{n} =====\n{qtxt}\n")

    src.close()

    index = {"paper": paper, "paper_full": paper_full,
             "questions": sorted(questions, key=lambda q: q["qnum"])}
    json_path = os.path.join("igcse-data", qp_stem + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    txt_path = os.path.join("igcse-data", qp_stem + ".questions.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"OK {qp_stem}: {len(questions)} questions -> {json_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
