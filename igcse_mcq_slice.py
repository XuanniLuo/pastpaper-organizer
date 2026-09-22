# -*- coding: utf-8 -*-
"""
Slice an IGCSE 0625 Paper 2 (Multiple Choice) question paper into one PDF per
question, parse the mark scheme for the answer letters, and emit a JSON index
(question number -> pdf, answer; topic code/name left blank for a later
categorization pass).

Usage:
    python igcse_mcq_slice.py igcse-2024/0625_m24_qp_22.pdf igcse-2024/0625_m24_ms_22.pdf

Outputs:
    igcse-slices/0625_m24_qp_22_Q01.pdf ... (40 slices)
    igcse-data/0625_m24_qp_22.json            (JSON index)
    igcse-data/0625_m24_qp_22.questions.txt   (extracted text for categorization)
"""
import json
import os
import re
import sys

import pymupdf

from igcse_syllabus import SUB_LABELS, TOPIC_TITLES, topic_of

SESSION = {"m": "F/M", "s": "M/J", "w": "O/N"}
SESSION_LABEL = {"m": "March", "s": "June", "w": "November"}

PAGE_W = 595.0
PAGE_H = 842.0
CONTENT_BOTTOM = 785.0   # just above the footer line (~793)
LEFT_MARGIN = 62.0       # question numbers sit at x~50; content labels are >=70

# Blocks matching these patterns are page furniture (footers, copyright /
# blank-page notices) and should not be captured as question content.
FOOTER_PATTERNS = re.compile(
    r"© UCLES|© Cambridge|Permission to reproduce|blank pages|\[Turn over",
    re.IGNORECASE,
)


def page_content_bottom(page, question_top):
    """Bottom y for the last question on a page: stop above any footer /
    copyright notice, otherwise the standard content bottom."""
    best = CONTENT_BOTTOM
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if y0 <= question_top:
            continue
        if y0 < best and FOOTER_PATTERNS.search(text):
            best = y0
    return best


def parse_paper_code(qp_stem):
    """'0625_m24_qp_22' -> ('0625/22/F/M/24', 'March 2024 · Paper 22')."""
    m = re.match(r"^(\d{4})_([msw])(\d{2})_qp_(\d{2})$", qp_stem)
    if not m:
        raise ValueError("cannot parse paper stem: " + qp_stem)
    code, session, yy, variant = m.group(1), m.group(2), m.group(3), m.group(4)
    year = "20" + yy
    paper = f"{code}/{variant}/{SESSION[session]}/{yy}"
    paper_full = f"{SESSION_LABEL[session]} {year} · Paper {variant}"
    return paper, paper_full


def find_question_numbers(doc):
    """Return {qnum: (page_index, y0)} for every question number 1-40."""
    found = {}
    for pi in range(len(doc)):
        page = doc[pi]
        for w in page.get_text("words"):
            x0, y0, _, _, word = w[0], w[1], w[2], w[3], w[4]
            t = word.strip()
            if t.isdigit() and 1 <= int(t) <= 40 and x0 < LEFT_MARGIN:
                n = int(t)
                # keep the first (topmost) occurrence — the question heading
                if n not in found:
                    found[n] = (pi, y0)
    return found


def slice_question(src_doc, page_index, top, bottom, out_path):
    clip = pymupdf.Rect(0, top, PAGE_W, bottom)
    w = PAGE_W
    h = max(bottom - top, 10)
    new_doc = pymupdf.open()
    new_page = new_doc.new_page(width=w, height=h)
    new_page.show_pdf_page(new_page.rect, src_doc, page_index, clip=clip)
    new_doc.save(out_path)
    new_doc.close()


def question_text(doc, page_index, top, bottom):
    page = doc[page_index]
    return page.get_text(clip=pymupdf.Rect(0, top, PAGE_W, bottom)).strip()


def parse_mark_scheme(ms_path):
    """Return {qnum: letter} parsed from the Question/Answer/Marks table."""
    doc = pymupdf.open(ms_path)
    answers = {}
    for page in doc:
        text = page.get_text()
        # table rows come out as "1 \nB \n1 \n2 \nB \n1 ..." — walk tokens
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        i = 0
        while i < len(lines) - 1:
            a, b = lines[i], lines[i + 1]
            if a.isdigit() and 1 <= int(a) <= 40 and re.fullmatch(r"[ABCD]", b):
                answers[int(a)] = b
                i += 1
            i += 1
    doc.close()
    return answers


def main(qp_path, ms_path):
    qp_stem = os.path.splitext(os.path.basename(qp_path))[0]
    paper, paper_full = parse_paper_code(qp_stem)

    src = pymupdf.open(qp_path)
    nums = find_question_numbers(src)

    if len(nums) < 40:
        missing = sorted(set(range(1, 41)) - set(nums))
        print(f"WARN: found {len(nums)}/40 question numbers; missing {missing}")

    # group numbers by page, ordered by y
    by_page = {}
    for n, (pi, y0) in nums.items():
        by_page.setdefault(pi, []).append((y0, n))
    for pi in by_page:
        by_page[pi].sort()

    answers = parse_mark_scheme(ms_path) if ms_path and os.path.exists(ms_path) else {}

    questions = []
    txt_lines = []
    for pi in sorted(by_page):
        items = by_page[pi]
        for k, (y0, n) in enumerate(items):
            top = max(y0 - 10.0, 0.0)
            if k + 1 < len(items):
                bottom = max(items[k + 1][0] - 10.0, top + 10.0)
            else:
                bottom = page_content_bottom(src[pi], top)
            pdf_name = f"{qp_stem}_Q{n:02d}.pdf"
            out_path = os.path.join("igcse-slices", pdf_name)
            slice_question(src, pi, top, bottom, out_path)
            qtxt = question_text(src, pi, top, bottom)
            questions.append({
                "qnum": n,
                "code": "",
                "topic_name": "",
                "answer": answers.get(n, ""),
                "pdf": "igcse-slices/" + pdf_name,
            })
            txt_lines.append(f"===== Q{n} (page {pi}) =====\n{qtxt}\n")

    src.close()

    index = {
        "paper": paper,
        "paper_full": paper_full,
        "questions": sorted(questions, key=lambda q: q["qnum"]),
    }
    json_path = os.path.join("igcse-data", qp_stem + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    txt_path = os.path.join("igcse-data", qp_stem + ".questions.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"OK {qp_stem}: {len(questions)} questions, {len(answers)} answers")
    print(f"   json: {json_path}")
    print(f"   text: {txt_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
