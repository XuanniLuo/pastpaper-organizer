# -*- coding: utf-8 -*-
"""
Slice an IGCSE 0625 Paper 4 (Theory) question paper into one PDF per question.

Each question number sits at the left margin (x~50). Questions normally start at
the top of a fresh page, but occasionally one starts mid-page (right after the
previous question's total). This script therefore detects every left-margin
question number and clips pages at mid-page boundaries so each slice contains
exactly one question. Blank pages are skipped.

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

TOP_Y = 100.0          # question numbers at page tops sit at y~61
LEFT_MARGIN = 62.0


def is_blank_page(page):
    text = page.get_text().strip()
    if "BLANK PAGE" in text.upper():
        return True
    compact = re.sub(r"\s+", " ", text)
    compact = compact.replace("© UCLES", "").replace("0625/", "").replace("[Turn over", "")
    compact = re.sub(r"\d+", "", compact).strip()
    return len(compact) < 4


def find_question_starts(doc):
    """Return {qnum: (page_index, y0)} for each question number 1-12.

    y0 is the top edge of the question-number word, used to clip mid-page
    question starts. Page numbers and figure/data values sit further right
    (x >= LEFT_MARGIN), so matching the left margin is unambiguous.
    """
    starts = {}
    for pi in range(1, len(doc)):   # skip cover (page 0)
        for w in doc[pi].get_text("words"):
            x0, y0, word = w[0], w[1], w[4]
            t = word.strip()
            if t.isdigit() and 1 <= int(t) <= 12 and x0 < LEFT_MARGIN:
                n = int(t)
                if n not in starts:
                    starts[n] = (pi, y0)
    return starts


def slice_pieces(src_doc, pieces, out_path):
    """Combine (page_index, clip_rect_or_None) pieces into one PDF."""
    new_doc = pymupdf.open()
    for pi, clip in pieces:
        src_page = src_doc[pi]
        rect = src_page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)
        new_page.show_pdf_page(new_page.rect, src_doc, pi, clip=clip)
    new_doc.save(out_path)
    new_doc.close()


def piece_text(src_doc, pieces):
    return "\n".join(
        src_doc[pi].get_text(clip=clip) if clip else src_doc[pi].get_text()
        for pi, clip in pieces
    )


def main(qp_path):
    qp_stem = os.path.splitext(os.path.basename(qp_path))[0]
    paper, paper_full = parse_paper_code(qp_stem)

    src = pymupdf.open(qp_path)
    starts = find_question_starts(src)
    ordered = sorted(starts.items())      # [(qnum, (pi, y0)), ...]

    last_pi = len(src) - 1
    while last_pi > 0 and is_blank_page(src[last_pi]):
        last_pi -= 1

    questions = []
    txt_lines = []
    for i, (n, (start_pi, start_y)) in enumerate(ordered):
        w = src[start_pi].rect.width
        h = src[start_pi].rect.height

        if i + 1 < len(ordered):
            _, (next_pi, next_y) = ordered[i + 1]
            if next_y >= TOP_Y:
                # next question starts mid-page -> this question's last page is clipped
                end_pi = next_pi
                end_clip = pymupdf.Rect(0, 0, w, next_y)
            else:
                end_pi = next_pi - 1
                end_clip = None
        else:
            end_pi = last_pi
            end_clip = None

        # build the (page, clip) pieces for this question
        pieces = []
        if start_y >= TOP_Y:
            pieces.append((start_pi, pymupdf.Rect(0, start_y, w, h)))
        else:
            pieces.append((start_pi, None))

        if end_pi > start_pi:
            for pi in range(start_pi + 1, end_pi):
                pieces.append((pi, None))
            pieces.append((end_pi, end_clip))
        elif end_pi == start_pi and start_y >= TOP_Y and end_clip is not None:
            # question fully contained on one page, between two mid-page numbers
            pieces = [(start_pi, pymupdf.Rect(0, start_y, w, next_y))]
        elif end_pi == start_pi and end_clip is not None:
            pieces = [(start_pi, end_clip)]

        pieces = [(pi, c) for pi, c in pieces if not is_blank_page(src[pi])]
        if not pieces:
            continue

        pdf_name = f"{qp_stem}_Q{n:02d}.pdf"
        out_path = os.path.join("igcse-slices", pdf_name)
        slice_pieces(src, pieces, out_path)

        qtxt = piece_text(src, pieces)
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
