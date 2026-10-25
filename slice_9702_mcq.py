# -*- coding: utf-8 -*-
"""
Slice a 9702 Paper 1 (Multiple Choice) question paper into one PDF per
question, extract each question's text (for later syllabus categorisation),
and parse the mark scheme for the answer letters.

Usage:
    python slice_9702_mcq.py 9702_s22_qp_11.pdf [9702_s22_ms_11.pdf]
    python slice_9702_mcq.py --all      # process every 2022/2023/2024 paper

Outputs (under _p1_work/):
    slices/{stem}_Q01.pdf ...           (one slice per question)
    text/{stem}.questions.txt           (question text for categorisation)
    {stem}.json                         (index: paper, questions[], answers)
"""
import json
import os
import re
import sys

import pymupdf

SESSION = {"m": "F/M", "s": "M/J", "w": "O/N"}
SESSION_LABEL = {"m": "March", "s": "June", "w": "November"}

PAGE_W = 595.0
PAGE_H = 842.0
CONTENT_BOTTOM = 785.0
LEFT_MARGIN = 62.0

WORK = "_p1_work"
SLICE_DIR = os.path.join(WORK, "slices")
TEXT_DIR = os.path.join(WORK, "text")

FOOTER_PATTERNS = re.compile(
    r"© UCLES|© Cambridge|Permission to reproduce|blank pages|\[Turn over",
    re.IGNORECASE,
)

# 2022/2023/2024 paper 1 qp stems
PAPERS = [
    "9702_m22_qp_12", "9702_s22_qp_11", "9702_s22_qp_12", "9702_s22_qp_13",
    "9702_w22_qp_11", "9702_w22_qp_12", "9702_w22_qp_13",
    "9702_m23_qp_12", "9702_s23_qp_11", "9702_s23_qp_12", "9702_s23_qp_13",
    "9702_w23_qp_11", "9702_w23_qp_12", "9702_w23_qp_13",
    "9702_m24_qp_12", "9702_s24_qp_11", "9702_s24_qp_12", "9702_s24_qp_13",
    "9702_w24_qp_11", "9702_w24_qp_12", "9702_w24_qp_13",
]


def parse_paper_code(qp_stem):
    m = re.match(r"^(\d{4})_([msw])(\d{2})_qp_(\d{2})$", qp_stem)
    code, session, yy, variant = m.group(1), m.group(2), m.group(3), m.group(4)
    year = "20" + yy
    paper = f"{code}/{variant}/{SESSION[session]}/{yy}"
    paper_full = f"{SESSION_LABEL[session]} {year} · Paper {variant}"
    return paper, paper_full


def page_content_bottom(page, question_top):
    best = CONTENT_BOTTOM
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if y0 <= question_top:
            continue
        if y0 < best and FOOTER_PATTERNS.search(text):
            best = y0
    return best


def find_question_numbers(doc):
    found = {}
    for pi in range(len(doc)):
        page = doc[pi]
        for w in page.get_text("words"):
            x0, y0, _, _, word = w[0], w[1], w[2], w[3], w[4]
            t = word.strip()
            if t.isdigit() and 1 <= int(t) <= 40 and x0 < LEFT_MARGIN:
                n = int(t)
                if n not in found:
                    found[n] = (pi, y0)
    return found


def slice_question(src_doc, page_index, top, bottom, out_path):
    clip = pymupdf.Rect(0, top, PAGE_W, bottom)
    h = max(bottom - top, 10)
    new_doc = pymupdf.open()
    new_page = new_doc.new_page(width=PAGE_W, height=h)
    new_page.show_pdf_page(new_page.rect, src_doc, page_index, clip=clip)
    new_doc.save(out_path)
    new_doc.close()


def question_text(doc, page_index, top, bottom):
    return doc[page_index].get_text(clip=pymupdf.Rect(0, top, PAGE_W, bottom)).strip()


def parse_mark_scheme(ms_path):
    doc = pymupdf.open(ms_path)
    answers = {}
    for page in doc:
        text = page.get_text()
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


def process(qp_stem, ms_stem=None):
    qp_path = f"{qp_stem}.pdf"
    ms_path = f"{ms_stem}.pdf" if ms_stem else qp_stem.replace("_qp_", "_ms_") + ".pdf"
    if not os.path.exists(ms_path):
        ms_path = None

    paper, paper_full = parse_paper_code(qp_stem)
    src = pymupdf.open(qp_path)
    nums = find_question_numbers(src)

    if len(nums) < 40:
        missing = sorted(set(range(1, 41)) - set(nums))
        print(f"WARN {qp_stem}: found {len(nums)}/40; missing {missing}")

    by_page = {}
    for n, (pi, y0) in nums.items():
        by_page.setdefault(pi, []).append((y0, n))
    for pi in by_page:
        by_page[pi].sort()

    answers = parse_mark_scheme(ms_path) if ms_path else {}

    questions = []
    txt_lines = []
    for pi in sorted(by_page):
        items = by_page[pi]
        for k, (y0, n) in enumerate(items):
            top = max(y0 - 10.0, 0.0)
            bottom = items[k + 1][0] - 10.0 if k + 1 < len(items) else page_content_bottom(src[pi], top)
            bottom = max(bottom, top + 10.0)
            pdf_name = f"{qp_stem}_Q{n:02d}.pdf"
            slice_question(src, pi, top, bottom, os.path.join(SLICE_DIR, pdf_name))
            qtxt = question_text(src, pi, top, bottom)
            questions.append({"qnum": n, "answer": answers.get(n, ""), "pdf": pdf_name})
            txt_lines.append(f"===== {qp_stem} Q{n} =====\n{qtxt}\n")

    src.close()

    questions.sort(key=lambda q: q["qnum"])
    index = {"paper": paper, "paper_full": paper_full, "questions": questions}
    with open(os.path.join(WORK, qp_stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    with open(os.path.join(TEXT_DIR, qp_stem + ".questions.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"OK {qp_stem}: {len(questions)} q, {len(answers)} answers")
    return len(questions), len(answers)


def main():
    os.makedirs(SLICE_DIR, exist_ok=True)
    os.makedirs(TEXT_DIR, exist_ok=True)

    if len(sys.argv) >= 2 and sys.argv[1] != "--all":
        qp = sys.argv[1]
        stem = os.path.splitext(os.path.basename(qp))[0]
        ms = sys.argv[2] if len(sys.argv) > 2 else None
        process(stem, os.path.splitext(os.path.basename(ms))[0] if ms else None)
        return

    total_q = 0
    for stem in PAPERS:
        n, a = process(stem)
        total_q += n
    print(f"\nDONE: {len(PAPERS)} papers, {total_q} questions")


if __name__ == "__main__":
    main()
