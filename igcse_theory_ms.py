# -*- coding: utf-8 -*-
"""
Parse an IGCSE 0625 Paper 4 mark scheme into per-question parts + answers + marks.

Usage:
    python igcse_theory_ms.py igcse-2024/0625_m24_ms_42.pdf [--json]

Prints a compact per-question summary; with --json writes
igcse-data/<stem>_ms.json.
"""
import json
import os
import re
import sys

import pymupdf

PART_RE = re.compile(r"^(\d+)(\(.+\))$")
MARK_RE = re.compile(r"^(A|B|C|M|E)\d+$")          # e.g. B1, A2, C1, M1
MARK_CLEAN = re.compile(r"\b[A-Z]\d\b")             # remove inline mark codes
HEADER_RE = re.compile(r"^(Question|Answer|Marks)$")


def collect_table_lines(ms_path):
    doc = pymupdf.open(ms_path)
    lines = []
    for pi in range(len(doc)):
        t = doc[pi].get_text()
        if "Marks" in t and ("Question" in t or "Answer" in t):
            for ln in t.splitlines():
                ln = ln.strip()
                if ln:
                    lines.append(ln)
    doc.close()
    return lines


def parse_parts(lines):
    """Split the flat line stream into [{qnum, label, answer, marks}]."""
    parts = []
    cur = None
    for ln in lines:
        m = PART_RE.match(ln)
        if m:
            if cur:
                parts.append(cur)
            cur = {"qnum": int(m.group(1)), "label": m.group(0),
                   "answer_lines": [], "marks": 0}
            continue
        if HEADER_RE.match(ln):
            continue
        if cur is None:
            continue
        if MARK_RE.match(ln):
            cur["marks"] += int(ln[1])
        else:
            cur["answer_lines"].append(ln)
    if cur:
        parts.append(cur)
    return parts


def clean_answer(lines):
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("(C1)", " ").replace("(A1)", " ").replace("(M1)", " ")
    text = re.sub(r"\(\s*[ABCME]\d\s*\)", " ", text)
    text = re.sub(r"\b[ABCME]\d\b", "", text)
    text = re.sub(r"\s+", " ", text).strip(" ,;")
    return text


def build_index(ms_path):
    lines = collect_table_lines(ms_path)
    parts = parse_parts(lines)
    by_q = {}
    for p in parts:
        q = by_q.setdefault(p["qnum"], {"qnum": p["qnum"], "marks": 0, "parts": []})
        q["marks"] += p["marks"]
        q["parts"].append({"label": p["label"], "marks": p["marks"],
                           "answer": clean_answer(p["answer_lines"])})
    return by_q


def main():
    ms_path = sys.argv[1]
    stem = os.path.splitext(os.path.basename(ms_path))[0].replace("_ms_", "_qp_")
    by_q = build_index(ms_path)
    if "--json" in sys.argv:
        out = os.path.join("igcse-data", stem + "_ms.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(by_q, f, ensure_ascii=False, indent=2)
        print("wrote", out)
    for qnum in sorted(by_q):
        q = by_q[qnum]
        print(f"Q{qnum}: {q['marks']} marks, {len(q['parts'])} parts")
        for p in q["parts"][:2]:
            print(f"   {p['label']} [{p['marks']}] {p['answer'][:80]}")


if __name__ == "__main__":
    main()
